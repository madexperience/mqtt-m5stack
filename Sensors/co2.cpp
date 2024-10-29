#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// Wi-Fi 설정
const char* ssid = "핫스팟";            // Wi-Fi 이름
const char* password = "1234567890q";  // Wi-Fi 비밀번호

// MQTT 브로커 설정
const char* mqtt_server = "test.mosquitto.org";
const char* gasTopic = "m5stack/gas";

// Wi-Fi 및 MQTT 클라이언트 객체
WiFiClient espClient;
PubSubClient client(espClient);

// MQ-9 센서의 Ro 값 (공기 중에서의 저항)
const float Ro = 10.0;

// 가스 농도 계산에 필요한 상수
const float methane_K = 120.0; // 메탄에 대한 K값
const float methane_n = 1.7;    // 메탄에 대한 n값
const float co_K = 75.0;        // 일산화탄소에 대한 K값
const float co_n = 1.9;         // 일산화탄소에 대한 n값
const float lpg_K = 85.0;       // LPG에 대한 K값
const float lpg_n = 2.1;        // LPG에 대한 n값

void setup() {
  Serial.begin(115200);        // 시리얼 통신 초기화
  pinMode(A0, INPUT);         // 아날로그 입력 설정
  setup_wifi();                // Wi-Fi 연결 설정
  client.setServer(mqtt_server, 1883);  // MQTT 서버 설정
  reconnect();  // 초기 MQTT 연결 시도
}

void setup_wifi() {
  WiFi.begin(ssid, password); // WiFi 연결 시작
  Serial.print("WiFi 연결 중");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\n WiFi 연결 완료");
  Serial.print("IP 주소: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  // MQTT 브로커에 연결
  while (!client.connected()) {
    Serial.print("MQTT 서버에 연결 중입니다...");
    if (client.connect("NodeMCUClient")) {
      Serial.println("connected");
    } else {
      Serial.print("오류 발생 : ");
      Serial.print(client.state());
      delay(2000);
    }
  }
}

void loop() {
  if (!client.connected()) {   // MQTT 연결 상태 확인
    reconnect();
  }
  client.loop();

  // 가스 센서 데이터 읽기
  int gasValue = analogRead(A0);        // 센서 값 읽기

  // MQ-9 센서의 저항 계산
  float R = (1023.0 / gasValue) - 1; // 저항 계산
  R = Ro / R; // Ro를 기준으로 변환

  // 메탄 농도 계산
  float methaneConcentration = pow(R, (1 / methane_n)) * methane_K;
  // 일산화탄소 농도 계산
  float coConcentration = pow(R, (1 / co_n)) * co_K;
  // LPG 농도 계산
  float lpgConcentration = pow(R, (1 / lpg_n)) * lpg_K;

  String gasData = "";

  // 가스 농도 출력
  Serial.print("메탄 농도: ");
  Serial.print(methaneConcentration);
  Serial.print(" ppm, ");
  Serial.print("일산화탄소 농도: ");
  Serial.print(coConcentration);
  Serial.print(" ppm, ");
  Serial.print("LPG 농도: ");
  Serial.print(lpgConcentration);
  Serial.println(" ppm");

  // 위험 조건 확인
  if (methaneConcentration >= 450 || coConcentration >= 250 || lpgConcentration >= 450) {
    gasData = "Danger"; // 위험 상태
  } else {
    gasData = "Safe"; // 안전 상태
  }

  client.publish(gasTopic, gasData.c_str()); // 문자열로 데이터 전송

  delay(1000); // 1초 대기
}