#ifndef AccelSensor_h
#define AccelSensor_h

#include <Arduino.h>
#include <MPU6050.h>
#include <Wire.h>

class AccelSensor {
  private:
    //int ledPin;
    //unsigned char ledState;
    MPU6050 mpu;

  public:
    int16_t ax, ay, az;
    AccelSensor();
    void setConfig();
    void getEvent();
};

#endif