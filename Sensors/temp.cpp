#include <DHT11.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

int pin = D1;
DHT11 dht11(pin);

const char* ssid = "KSM";
const char* password = "ksm!@1419";

const char* mqtt_server = "test.mosquitto.org";

WiFiClient espClient;
PubSubClient client(espClient);

unsigned long lastMsgTime = 0; 

void setup() {
  Serial.begin(115200); 
  setup_wifi();         
  
  client.setServer(mqtt_server, 1883); 
  reconnect(); 
}

void setup_wifi() {
  WiFi.begin(ssid, password);
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
  while (!client.connected()) {
    Serial.print("MQTT 서버에 연결 중...");
    if (client.connect("NodeMCUClient")) {
      Serial.println("연결 성공");
    } else {
      Serial.print("오류 코드: ");
      Serial.print(client.state());
      delay(2000);
    }
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  unsigned long now = millis();
  if (now - lastMsgTime > 1000) {
    lastMsgTime = now;

    int err;
    float temp, humi;
    const char* tempTopic = "m5stack/temperature";

    if ((err = dht11.read(humi, temp)) == 0) {
      Serial.print("현재 기온: ");
      Serial.print(temp);
      Serial.print(" °C, ");
      Serial.print("현재 습도: ");
      Serial.print(humi);
      Serial.println(" %");

      char tempStr[8];
      dtostrf(temp, 6, 2, tempStr);
      client.publish(tempTopic, tempStr);

    } else {
      Serial.print("DHT11 센서 오류 코드: ");
      Serial.println(err);
    }
  }
}