#ifndef WifiConnect_h
#define WifiConnect_h
#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <Arduino_JSON.h>


class WifiConnect {
public:

    WifiConnect();
    void WifiSetup(char* ssid,char* password);
    void HttpRegister();
    void HttpPostAccel(String, String, String);
	
private:

  
};
#endif