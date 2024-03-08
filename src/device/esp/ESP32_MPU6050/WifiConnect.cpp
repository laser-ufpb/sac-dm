#include <Arduino.h>
#include "WifiConnect.h"

WifiConnect::WifiConnect() {

  
}

void WifiConnect::WifiSetup(char* ssid, char* password) {

  Serial.begin(115200);

  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());

  Serial.end();

}
void WifiConnect::HttpRegister(){

  const char* server_name = "https://enmpf6xid68v.x.pipedream.net/" ;

if(WiFi.status()== WL_CONNECTED){  

  HTTPClient http;

  http.begin(server_name);

  http.addHeader("Content-Type", "application/json");

  int httpResponseCode = http.POST("{\"mac_adress\":\""+ WiFi.macAddress() +"\",\"device_type\":\"esp32\"}");

  Serial.print("HTTP Response code: ");
  Serial.println(httpResponseCode);

  http.end();  

}else
Serial.println("Wifi Disconnected");
}
void WifiConnect::HttpPostAccel(String AcclX, String AcclY, String AcclZ){

  //https://enmpf6xid68v.x.pipedream.net/
  //https://test-implantacao.rj.r.appspot.com/accelerometer

  const char* server_name = "https://enmpf6xid68v.x.pipedream.net/" ;

if(WiFi.status()== WL_CONNECTED){  

  Serial.begin(115200);

  HTTPClient http;

  http.begin(server_name);

  http.addHeader("Content-Type", "application/json");

  String data;
  
  data = "{\"device_code\":\"01\",\"ACx\":\"" + AcclX + "\",\"ACy\":\"" + AcclY + " \",\"ACz\":\"" + AcclZ + "\"}";

  int httpResponseCode = http.POST(data);

  Serial.print("HTTP Response code: ");
  Serial.println(httpResponseCode);

  http.end();  

}else
  Serial.println("Wifi Disconnected");
}

