#ifndef WifiConnect_h
#define WifiConnect_h
#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <PubSubClient.h>
#include <Arduino_JSON.h>


class WifiConnect {
public:

  WifiConnect();
  void WifiSetup(char*, char*);
  void MqttSetup(char*, int);
  void MqttPublish(char*, String);
  void MqttLoop();
	
private:
  
  const char* ssid = "SSID"; 
  const char* password = "SENHA"; 
  
};
#endif