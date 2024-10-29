#include <M5Core2.h>
#include <WiFi.h>
#include <WiFiUdp.h>
#include <NTPClient.h>
#include <PubSubClient.h>

const char* ssid = "KSM";
const char* password = "ksm!@1419";

const char* mqtt_server = "test.mosquitto.org";
const char* tempTopic =  "m5stack/temperature";
const char* gasTopic = "m5stack/gas";

const int temp_threshold = 45;

WiFiUDP udp;
NTPClient timeClient(udp, "pool.ntp.org", 9 * 3600); 

float tempValue = 0.0;  
String gasValue =" ";

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  M5.begin();
  M5.Lcd.setTextSize(2);
  M5.Lcd.setCursor(10, 10);
  M5.Lcd.println("Connecting to WiFi...");

  setup_wifi();               
  timeClient.begin();        
  timeClient.update();       
  
  client.setServer(mqtt_server, 1883);  
  client.setCallback(callback);         

  while (!client.connected()) {     
    if (client.connect("M5Core2Client")) {  
      client.subscribe(tempTopic);
      client.subscribe(gasTopic);
    } else {
      delay(2000);
    }
  }
}

void setup_wifi() {
  WiFi.begin(ssid, password);  

  while (WiFi.status() != WL_CONNECTED) {  
    delay(500);
    M5.Lcd.print(".");
  }

  M5.Lcd.println("WiFi connected");
}

void displayTime() {
    timeClient.update(); 
    String formattedTime = timeClient.getFormattedTime(); 

    M5.Lcd.setCursor(50, 10); 
    M5.Lcd.setTextColor(WHITE);
    M5.Lcd.print("Time: ");
    M5.Lcd.println(formattedTime); 
}

void callback(char* topic, byte* payload, unsigned int length) {
  String message;

  for (int i = 0; i < length; i++) {
    message += (char)payload[i];  
  }

  Serial.print("Received raw message: ");
  Serial.print("Topic:");
  Serial.print(topic);
  Serial.print("massge: ");
  Serial.println(message);  

  if (String(topic) == tempTopic) {
    tempValue = message.toFloat();
    Serial.print("temp value:");
    Serial.println(tempValue);
  }else if (String(topic) == gasTopic) {
     gasValue = message;
     Serial.print("gas value:");
     Serial.println(gasValue);  
  }
  
  M5.Lcd.fillScreen(BLACK); 
  displayTime(); 

  M5.Lcd.setCursor(50, 80);
  M5.Lcd.setTextColor(WHITE);
  M5.Lcd.setTextSize(2);
  M5.Lcd.println("Temperature: " + String(tempValue)); 

  M5.Lcd.setCursor(50, 100);
  M5.Lcd.println("Gas Level: ");

  M5.Lcd.setCursor(170, 100);
  M5.Lcd.setTextColor(GREEN);
  M5.Lcd.println(gasValue);  
 
  if (tempValue >= temp_threshold) {
    M5.Lcd.fillScreen(BLACK);
    M5.Lcd.setCursor(50, 110);
    M5.Lcd.setTextColor(RED);   
    M5.Lcd.setTextSize(2);
    M5.Lcd.println("High Temperature Alert!");
    M5.Lcd.setCursor(50, 120);
    M5.Lcd.println("Temperature: " + String(tempValue)); 
    M5.Axp.SetLDOEnable(3, true); 
    delay(2000);                  
    M5.Axp.SetLDOEnable(3, false);
  }  

  if (gasValue == "Denger") {
    M5.Lcd.fillScreen(BLACK);
    M5.Lcd.setCursor(50, 130);
    M5.Lcd.setTextColor(RED); 
    M5.Lcd.setTextSize(2);
    M5.Lcd.println("Gas Leak Alert!");
    M5.Lcd.setCursor(50, 150);
    M5.Lcd.println("Gas Level: " + String(gasValue)); 
    M5.Axp.SetLDOEnable(3, true); 
    delay(2000);                  
    M5.Axp.SetLDOEnable(3, false);
  }
}

void loop() {
  if (!client.connected()) {
    while (!client.connected()) {
      if (client.connect("M5Core2Client")) {
        client.subscribe(tempTopic); 
        client.subscribe(gasTopic);
      }
      delay(2000);
    }
  }
  client.loop(); 

    displayTime();
    delay(1000);
}