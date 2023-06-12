#include "WifiConnect.h"
#include "AccelSensor.h"

int16_t ax_list[10000];
int16_t ay_list[10000];
int16_t az_list[10000];

AccelSensor accel;
int i;

// Serial and Accelerometer sensor configuration
void setup() {
  Serial.begin(115200);
  accel.setConfig();

}
void loop() {

  // Store 10.000 sensor data in the buffer
  for(i=0; i < 10000; i++){
    accel.getEvent();
    ax_list[i] = accel.ax;
    ay_list[i] = accel.ay;
    az_list[i] = accel.az;

  }

  // Send all buffer by serial communication
  for( i=0; i < 10000; i++){
    Serial.println(String(ax_list[i]) +","+ String(ay_list[i]) +","+ String(az_list[i]));

  }
  
  // Lock the ESP32 in an infinite loop to stop its execution
  while(1){}
  
}