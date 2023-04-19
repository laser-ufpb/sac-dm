#include "WifiConnect.h"
#include "AccelSensor.h"

WifiConnect wifi;
AccelSensor accel;

void setup() {
  
  wifi.WifiSetup("iPhone de Francisco", "xgdkmomw6");
  accel.setConfig();
  //wifi.HttpRegister();
}

void loop() {

  accel.getEvent();
  wifi.HttpPostAccel(String(accel.a.acceleration.x), String(accel.a.acceleration.y), String(accel.a.acceleration.z));


  delay(5000);

  
}