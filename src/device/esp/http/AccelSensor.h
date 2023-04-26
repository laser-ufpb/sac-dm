#ifndef AccelSensor_h
#define AccelSensor_h

#include <Arduino.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

class AccelSensor {
  private:
    //int ledPin;
    //unsigned char ledState;
    Adafruit_MPU6050 mpu;

  public:
    sensors_event_t a, g, temp;
    AccelSensor();
    void setConfig();
    void getEvent();
};

#endif