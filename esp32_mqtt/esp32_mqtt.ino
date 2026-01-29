#include "secrets.h"
#include <WiFiClientSecure.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include "WiFi.h"

#define LEDPIN 23
#define BTNPIN 14
#define BTNTYPE INPUT
 
#define AWS_IOT_PUBLISH_TOPIC   "esp32/pub"
#define AWS_IOT_SUBSCRIBE_TOPIC "esp32/sub"
 
WiFiClientSecure net = WiFiClientSecure();
PubSubClient client(net);

int f;




#include <ESP32Servo.h>

// Define the servo object
Servo servo11;
Servo servo12;
Servo servo13;
Servo servo21;
Servo servo22;
Servo servo23;

// Define the GPIO pin for the servo signal
const int8_t servo11pin = 13;
const int8_t servo12pin = 12;
const int8_t servo13pin = 14;
const int8_t servo21pin = 27;
const int8_t servo22pin = 26;
const int8_t servo23pin = 25;

const int8_t init_flower = 50;
const int8_t init_stem = 90;
const int8_t flower_max = 90;
const int8_t flower_min = 30;
const int8_t stem_max = 90;
const int8_t stem_min = 10;
// const int8_t heat1 = 25;

// Define servo angle limits
// const int8_t minAngle = 0;
// const int8_t maxAngle = 180;

const int inputPin1 = 32;
const int inputPin2 = 33;

// void ledOn(int lightOn)
// {
//   digitalWrite(vibrate1, HIGH);  // turn the LED on (HIGH is the voltage level)
//   delay(lightOn);                      // wait for a second
//   digitalWrite(vibrate1, LOW);   // turn the LED off by making the voltage LOW
//   delay(1000);
// }
 
void connectAWS()
{

  // Start Wi-Fi scan
  Serial.println("Scanning for Wi-Fi networks...");
  int numberOfNetworks = WiFi.scanNetworks();
  
  if (numberOfNetworks == 0) {
    Serial.println("No networks found.");
  } else {
    Serial.println("Networks found:");
    for (int i = 0; i < numberOfNetworks; ++i) {
      Serial.print(i + 1);
      Serial.print(": ");
      Serial.print(WiFi.SSID(i));
      Serial.print(" (");
      Serial.print(WiFi.RSSI(i));
      Serial.print(" dBm)");
      Serial.println();
      delay(10);
    }
  }
  
  Serial.println("Scan complete.");

  WiFi.mode(WIFI_STA);
  // WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  WiFi.begin(WIFI_SSID, WPA2_AUTH_PEAP, WIFI_ID, WIFI_ID, WIFI_PASSWORD);
  
  Serial.println("Connecting to Wi-Fi");
  

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
 
  // Configure WiFiClientSecure to use the AWS IoT device credentials
  net.setCACert(AWS_CERT_CA);
  net.setCertificate(AWS_CERT_CRT);
  net.setPrivateKey(AWS_CERT_PRIVATE);
 
  // Connect to the MQTT broker on the AWS endpoint we defined earlier
  client.setServer(AWS_IOT_ENDPOINT, 8883);
 
  // Create a message handler
  client.setCallback(messageHandler);
 
  Serial.println("Connecting to AWS IOT");
 
  while (!client.connect(THINGNAME))
  {
    Serial.print(".");
    delay(100);
  }
 
  if (!client.connected())
  {
    Serial.println("AWS IoT Timeout!");
    return;
  }
 
  // Subscribe to a topic
  client.subscribe(AWS_IOT_SUBSCRIBE_TOPIC);
 
  Serial.println("AWS IoT Connected!");
}
 
void publishMessage()
{
  StaticJsonDocument<200> doc;
  doc["message"] = "chris";
  char jsonBuffer[512];
  serializeJson(doc, jsonBuffer); // print to client
 
  client.publish(AWS_IOT_PUBLISH_TOPIC, jsonBuffer);
}
 
void messageHandler(char* topic, byte* payload, unsigned int length)
{
  Serial.print("incoming: ");
  Serial.println(topic);
 
  StaticJsonDocument<200> doc;
  deserializeJson(doc, payload);
  const char* message = doc["message"];
  Serial.println(message);
  Serial.println("message");

  

  // servo1.write(atoi(message));
  // leaf_attack(atoi(message));
  // electric_attack(atoi(message));

  if (atoi(message) == 0) {
    servo11.write(30);
    servo21.write(90);
    delay(50);
    servo11.write(40);
    servo21.write(80);
    delay(50);
    servo11.write(50);
    servo21.write(70);
    delay(50);
    servo11.write(60);
    servo21.write(50);
    delay(50);
    servo11.write(70);
    servo21.write(40);
    delay(50);
    servo11.write(80);
    servo21.write(20);
    delay(50);
    servo11.write(90);
    servo21.write(10);
    delay(50);
    
    delay(500);
  }

  else if (atoi(message) == 1) {
    servo12.write(30);
    servo22.write(90);
    delay(50);
    servo12.write(40);
    servo22.write(80);
    delay(50);
    servo12.write(50);
    servo22.write(70);
    delay(50);
    servo12.write(60);
    servo22.write(50);
    delay(50);
    servo12.write(70);
    servo22.write(40);
    delay(50);
    servo12.write(80);
    servo22.write(20);
    delay(50);
    servo12.write(90);
    servo22.write(10);
    delay(50);
    
    delay(500);
  }

  else if (atoi(message) == 2) {
    servo13.write(30);
    servo23.write(90);
    delay(50);
    servo13.write(40);
    servo23.write(80);
    delay(50);
    servo13.write(50);
    servo23.write(70);
    delay(50);
    servo13.write(60);
    servo23.write(50);
    delay(50);
    servo13.write(70);
    servo23.write(40);
    delay(50);
    servo13.write(80);
    servo23.write(20);
    delay(50);
    servo13.write(90);
    servo23.write(10);
    delay(50);
    
    delay(500);
  }

  else if (atoi(message) == 4) {
    servo11.write(90);
    servo21.write(10);
    delay(50);
    servo11.write(80);
    servo21.write(20);
    delay(50);
    servo11.write(70);
    servo21.write(40);
    delay(50);
    servo11.write(60);
    servo21.write(50);
    delay(50);
    servo11.write(50);
    servo21.write(70);
    delay(50);
    servo11.write(40);
    servo21.write(80);
    delay(50);
    servo11.write(30);
    servo21.write(90);
    delay(50);
    
    delay(500);
  }

  else if (atoi(message) == 5) {
    servo12.write(90);
    servo22.write(10);
    delay(50);
    servo12.write(80);
    servo22.write(20);
    delay(50);
    servo12.write(70);
    servo22.write(40);
    delay(50);
    servo12.write(60);
    servo22.write(50);
    delay(50);
    servo12.write(50);
    servo22.write(70);
    delay(50);
    servo12.write(40);
    servo22.write(80);
    delay(50);
    servo12.write(30);
    servo22.write(90);
    delay(50);
    
    delay(500);
  }

  else if (atoi(message) == 6) {
    servo13.write(90);
    servo23.write(10);
    delay(50);
    servo13.write(80);
    servo23.write(20);
    delay(50);
    servo13.write(70);
    servo23.write(40);
    delay(50);
    servo13.write(60);
    servo23.write(50);
    delay(50);
    servo13.write(50);
    servo23.write(70);
    delay(50);
    servo13.write(40);
    servo23.write(80);
    delay(50);
    servo13.write(30);
    servo23.write(90);
    delay(50);
    
    delay(500);
  }

  else if (atoi(message) == 7) {
    servo11.write(30);
    delay(50);
    servo11.write(40);
    delay(50);
    servo11.write(50);
    delay(50);
    servo11.write(60);
    delay(50);
    servo11.write(70);
    delay(50);
    servo11.write(80);
    delay(50);
    servo11.write(90);
    delay(50);
    
    delay(500);
  }

  else if (atoi(message) == 8) {
    servo11.write(90);
    delay(50);
    servo11.write(80);
    delay(50);
    servo11.write(70);
    delay(50);
    servo11.write(60);
    delay(50);
    servo11.write(50);
    delay(50);
    servo11.write(40);
    delay(50);
    servo11.write(30);
    delay(50);
    
    delay(500);
  }

  else if (atoi(message) == 9) {
    servo11.write(30);
    servo21.write(90);
    servo12.write(30);
    servo22.write(90);
    servo13.write(30);
    servo23.write(90);
    delay(50);
    servo11.write(40);
    servo21.write(80);
    servo12.write(40);
    servo22.write(80);
    servo13.write(40);
    servo23.write(80);
    delay(50);
    servo11.write(50);
    servo21.write(70);
    servo12.write(50);
    servo22.write(70);
    servo13.write(50);
    servo23.write(70);
    delay(50);
    servo11.write(60);
    servo21.write(50);
    servo12.write(60);
    servo22.write(50);
    servo13.write(60);
    servo23.write(50);
    delay(50);
    servo11.write(70);
    servo21.write(40);
    servo12.write(70);
    servo22.write(40);
    servo13.write(70);
    servo23.write(40);
    delay(50);
    servo11.write(80);
    servo21.write(20);
    servo12.write(80);
    servo22.write(20);
    servo13.write(80);
    servo23.write(20);
    delay(50);
    servo11.write(90);
    servo21.write(10);
    servo12.write(90);
    servo22.write(10);
    servo13.write(90);
    servo23.write(10);
    delay(50);
    
    delay(500);
  }

  else if (atoi(message) == 10) {
    servo11.write(90);
    servo21.write(10);
    servo12.write(90);
    servo22.write(10);
    servo13.write(90);
    servo23.write(10);
    delay(50);
    servo11.write(80);
    servo21.write(20);
    servo12.write(80);
    servo22.write(20);
    servo13.write(80);
    servo23.write(20);
    delay(50);
    servo11.write(70);
    servo21.write(40);
    servo12.write(70);
    servo22.write(40);
    servo13.write(70);
    servo23.write(40);
    delay(50);
    servo11.write(60);
    servo21.write(50);
    servo12.write(60);
    servo22.write(50);
    servo13.write(60);
    servo23.write(50);
    delay(50);
    servo11.write(50);
    servo21.write(70);
    servo12.write(50);
    servo22.write(70);
    servo13.write(50);
    servo23.write(70);
    delay(50);
    servo11.write(40);
    servo21.write(80);
    servo12.write(40);
    servo22.write(80);
    servo13.write(40);
    servo23.write(80);
    delay(50);
    servo11.write(30);
    servo21.write(90);
    servo12.write(30);
    servo22.write(90);
    servo13.write(30);
    servo23.write(90);
    delay(50);
    
    delay(500);
  }
  
  else if (atoi(message)) {
    servo11.write(atoi(message));
    servo12.write(atoi(message));
    servo13.write(atoi(message));
    servo21.write(atoi(message));
    servo22.write(atoi(message));
    servo23.write(atoi(message));
    delay(500);
  }
  


}

void setup()
{
  Serial.begin(115200);
  connectAWS();

  // Attach the servo to the GPIO pin
  servo11.attach(servo11pin);
  servo12.attach(servo12pin);
  servo13.attach(servo13pin);
  servo21.attach(servo21pin);
  servo22.attach(servo22pin);
  servo23.attach(servo23pin);
  


  // // Set the initial position of the servo
  // servo11.write(init_flower); // Middle position
  // servo12.write(init_flower); // Middle position
  // servo13.write(init_flower); // Middle position

  // servo21.write(init_stem); // Middle position
  // servo22.write(init_stem); // Middle position
  // servo23.write(init_stem); // Middle position

  delay(1000); // Wait for the servo to reach the position
}
 
void loop()
{
  int inputState1 = touchRead(inputPin1); // Read the digital state (HIGH or LOW)
  int inputState2 = touchRead(inputPin2);
  Serial.print("Digital Input on pin ");
  Serial.print(inputPin1);
  Serial.print(": ");
  Serial.print(inputState1);
  Serial.println(inputState2);
  // potValue = analogRead(potPin);
  // Serial.print("Analog value: ");
  // Serial.println(potValue);

  if(Serial.available() > 0)  {
    int incomingData = Serial.parseInt();
    Serial.print("incomingData: ");
    Serial.println(incomingData);
    if (incomingData >= 10) {
      servo11.write(incomingData);
      servo12.write(incomingData);
      servo13.write(incomingData);
      servo21.write(incomingData);
      servo22.write(incomingData);
      servo23.write(incomingData);
      delay(1000);
    }
  }

  if (inputState1 <= 28) {
    Serial.print("pin ");
    Serial.print(inputPin1);
    Serial.print(": ");
    Serial.print(inputState1);

    servo11.write(30);
    servo21.write(30);
    delay(1000);
    publishMessage();
  }

  if (inputState2 <= 28) {
    Serial.print("pin ");
    Serial.print(inputPin2);
    Serial.print(": ");
    Serial.print(inputState2);

    servo13.write(30);
    servo23.write(30);
    delay(1000);
    publishMessage();
  }
  // servoAngle = map(potValue, 0, 4095, 0, 180);
  // servo2pin.write(servoAngle);

  // int buttonState = digitalRead(BTNPIN);
  // digitalWrite(LEDPIN, LOW);

  // if (buttonState == LOW) { // Button pressed (active low)
  //   digitalWrite(LEDPIN, HIGH); // Turn on vibration
  // } else {
  //   digitalWrite(LEDPIN, LOW);  // Turn off vibration
  // }
 
  // Serial.println(F("LOOP"));
 
  // publishMessage();

  client.loop();
  delay(10); 
}



