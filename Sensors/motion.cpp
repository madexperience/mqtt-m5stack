#include <ESP8266WiFi.h>
#include <PubSubClient.h>

int Pin = D5;               
int pirState = LOW;       

const char* ssid = "DIT_CS_AI";         
const char* password = "ditcsai001"; 

const char* mqtt_server = "test.mosquitto.org"; 

WiFiClient espClient;
PubSubClient client(espClient);

unsigned long lastMsgTime = 0;

void setup() {
  pinMode(Pin, INPUT);         
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

  Serial.println("\nWiFi 연결 완료");
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

    int motionDetected = digitalRead(Pin);
    const char* motionTopic = "m5stack/motion";

    if (motionDetected != pirState) {
      if (motionDetected == HIGH) {
        Serial.println("움직임 감지!");
        client.publish(motionTopic, "Motion Detected!");
      } else {
        Serial.println("움직임 없음");
        client.publish(motionTopic, "No Motion Detected");
      }
      pirState = motionDetected;
    }
  }
}