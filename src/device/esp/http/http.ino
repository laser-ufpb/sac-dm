#include "WifiConnect.h"
#include <Arduino.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <time.h>

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

int receiverCounter = 0; // Counter for accelerometer readings
int transmitterCounter = 0; // Counter for queue writes

unsigned long startTime;
unsigned long elapsedTime;
int countX = 0;
int countY = 0;
int countZ = 0;

void setup()
{
  Serial.begin(115200);

  if (!mpu.begin())
  {
    while (1)
    {
      delay(10);
    }
  }
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_5_HZ);

  accerQueue = xQueueCreate(NO_OF_SAMPLES, sizeof(accer_st));
  xTaskCreate(&transmitter, "transmitter", 2 * 1024, NULL, 2, NULL);
  xTaskCreate(&receiver, "receiver", 2 * 1024, NULL, 2, NULL);
}

void loop()
{

}

void countTime(){
   // Counting X, Y, and Z prints
    countX++;
    countY++;
    countZ++;

    // Measure time and reset count every second
    if (millis() - startTime >= 1000)
    {
      Serial.println("Number of X prints in 1 second: " + String(countX));
      Serial.println("Number of Y prints in 1 second: " + String(countY));
      Serial.println("Number of Z prints in 1 second: " + String(countZ));

      countX = 0;
      countY = 0;
      countZ = 0;
      startTime = millis();
    }
  }



void transmitter(void *pvParameters)
{
  int availableSpaces = 0;
  accer_st accerReceived;

  while (true)
  {
    xQueueReceive(accerQueue, &accerReceived, portMAX_DELAY);
  }
}


void receiver(void *pvParameters)
{
  while (true)
  {
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);

    currentData.x = a.acceleration.x;
    currentData.y = a.acceleration.y;
    currentData.z = a.acceleration.z;

    xQueueSend(accerQueue, &currentData, portMAX_DELAY);
    countTime();
   
  }
  vTaskDelay(pdMS_TO_TICKS(100));
}