#include "AccelSensor.h"

char ch;
int incomingbyte = 0;

AccelSensor::AccelSensor() {

}

void AccelSensor::getEvent() {

  mpu.getAcceleration(&ax, &ay, &az);

}
void AccelSensor::setConfig() {

  Wire.begin();
  mpu.initialize();

  delay(100);

}