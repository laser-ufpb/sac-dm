#include "WifiConnect.h"
#include "AccelSensor.h"

// Sensor reading type struct
typedef struct {
int16_t ax;
int16_t ay;
int16_t az;

} SensorList;


AccelSensor accel;
SensorList data_buffer[100000];

// Serial and Accelerometer sensor configuration
void setup() {
  Serial.begin(115200);
  accel.setConfig();

}
void loop() {

  // Store 100.000 sensor data in the buffer
  for(int i=0; i< sizeof(data_buffer); i++){
    accel.getEvent();
    data_buffer[i].ax = accel.ax;
    data_buffer[i].ay = accel.ay;
    data_buffer[i].az = accel.az;

  }

  // Send all buffer by serial communication
  for(int i=0; i< sizeof(data_buffer); i++){
    Serial.println(String(data_buffer[i].ax) +","+ String(data_buffer[i].ay) +","+ String(data_buffer[i].az));

  }
  
  // Lock the ESP32 in an infinite loop to stop its execution
  while(1){}
  
}