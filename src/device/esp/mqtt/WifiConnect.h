#ifndef WifiConnect_h
#define WifiConnect_h
#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <PubSubClient.h>
#include <Arduino_JSON.h>

class WifiConnect
{
public:
  WifiConnect();
  void WifiSetup(char *, char *);
  void HttpRegister();
  void HttpPostAccel(String, String, String);
  void MqttSetup(char *, int);
  void MqttPublish(char *, String);
  void Reconnect(char *);
  void ConnectMqtt(char *);
  void MqttLoop();

private:
};
#endif
