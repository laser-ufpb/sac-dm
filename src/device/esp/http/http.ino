#include "WifiConnect.h"
#include <Arduino.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

#define NO_OF_SAMPLES 200
Adafruit_MPU6050 mpu;
QueueHandle_t accerQueue;

typedef struct 
{
  float x;
  float y;
  float z;
} accer_st;

accer_st currentData;

int i, j;

// Serial and Accelerometer sensor configuration
void setup() {
  Serial.begin(115200);

  if (!mpu.begin()) {
    while (1) {
      delay(10);
    }
  }
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_5_HZ);
  // delay(100);

  accerQueue = xQueueCreate(NO_OF_SAMPLES, sizeof(accer_st));
  xTaskCreate(&transmitter, "transmitter", 2*1024, NULL, 2, NULL);
  xTaskCreate(&receiver, "receiver", 2*1024, NULL, 2, NULL);
}

void loop() {

  
}

void transmitter(void *pvParameters)
{
  int availableSpaces = 0;
  accer_st accerReceived;

  while(true)
  {
    xQueueReceive(accerQueue, &accerReceived, portMAX_DELAY);
    Serial.println(String(accerReceived.x) +","+ String(accerReceived.y) +","+ String(accerReceived.z));
    // vTaskDelay(pdMS_TO_TICKS(10));
    // Serial.println(String(w) + " - " + String(uxQueueSpacesAvailable(accerQueue)) +" - "+String(accerReceived.x) +","+ String(accerReceived.y) +","+ String(accerReceived.z)); 
  }
}

void receiver(void *pvParameters)
{
  while(true)
  {
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);

    currentData.x = a.acceleration.x;
    currentData.y = a.acceleration.y;
    currentData.z = a.acceleration.z;
    
    xQueueSend(accerQueue, &currentData, portMAX_DELAY);
    // vTaskDelay(pdMS_TO_TICKS(10));
  }
}