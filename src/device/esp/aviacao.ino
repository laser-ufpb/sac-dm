#include "WifiConnect.h"
#include "AccelSensor.h"

WifiConnect wifi;
AccelSensor accel;

void setup() {
  
  wifi.WifiSetup("iPhone de Francisco", "xgdkmomw6");
  accel.setConfig();
  //wifi.HttpRegister();


  accel.getEvent();

  delay(50);

  wifi.HttpPostAccel(String(accel.a.acceleration.x), String(accel.a.acceleration.y), String(accel.a.acceleration.z));
  
  
}

void loop() {
  
  //Serial.begin(9600);
    
  //String data;


  //data = String(accel.a.acceleration.x) + "," + String(accel.a.acceleration.y) + "," + String(accel.a.acceleration.z);
  
  //Serial.println(data);

  //delay(5000);

  
}