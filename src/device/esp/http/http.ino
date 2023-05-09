#include "WifiConnect.h"
#include "AccelSensor.h"

WifiConnect wifi;
AccelSensor accel;
String data;

void setup() {

  Serial.begin(115200);
  //wifi.WifiSetup("iPhone de Francisco", "xgdkmomw6");
  accel.setConfig();
  
  
}
//unsigned long start = millis();
//int count=0;
void loop() {

  accel.getEvent();
  data = String(accel.ax) +","+ String(accel.ay) +","+ String(accel.az);
  Serial.println(data);
  //count++;
/*
  if((millis()- start)>=10000){
    Serial.print(count);
    while(1){}
  }

  */

  //wifi.HttpPostAccel(String(accel.a.acceleration.x), String(accel.a.acceleration.y), String(accel.a.acceleration.z));
  //delay(1000);


  
}