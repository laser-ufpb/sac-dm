#include <Arduino.h>
#include "WifiConnect.h"

WiFiClient espClient;
PubSubClient MQTT(espClient);

void check_connection_wifi(){

  if(WiFi.status() == WL_CONNECTED) return;

  while(WiFi.status() != WL_CONNECTED) {
    delay(100);
  }  
}
void check_connection_mqtt(char* broker_topic) {
  if(MQTT.connected()) return;
  
  while (!MQTT.connected()) {
    
    if (MQTT.connect("esp32_client_mqtt")) 
      MQTT.subscribe(broker_topic);  
    else 
      delay(2000);

  }
}

void mqtt_callback(char* topic, byte* payload, unsigned int length) {
  //Serial.begin(115200);
  String msg;

  for(int i = 0; i < length; i++) {
    char c = (char)payload[i];
    msg += c;
  }
  //Serial.print("[MQTT] Callback: ");
  //Serial.println(msg);     
  //Serial.end();    
}

WifiConnect::WifiConnect() {}

void WifiConnect::WifiSetup(char* SSID, char* PASSWORD) {

  ssid = SSID;
  password = PASSWORD;

  WiFi.begin(ssid, password);
  check_connection_wifi();


}
void WifiConnect::MqttSetup(char* broker_url, int broker_port){

  MQTT.setServer(broker_url, broker_port); 
  MQTT.setCallback(mqtt_callback); 

}

void WifiConnect::MqttPublish(char* broker_topic, String data){

  check_connection_mqtt(broker_topic);
  const char* pub = data.c_str();
  
  MQTT.publish(broker_topic, pub);

}

void WifiConnect::MqttLoop(){
  MQTT.loop();  
}
