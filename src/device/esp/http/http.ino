#include "AccelSensor.h"

AccelSensor accel;

void setup(void) {

  Serial.begin(115200);
  accel.setConfig();

}

void loop() {

  String data;
  accel.getEvent();
  data = String(accel.ax) + ";" + String(accel.ay) + ";" + String(accel.az);

  Serial.println(data);
}