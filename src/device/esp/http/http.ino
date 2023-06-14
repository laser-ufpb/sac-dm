#include "WifiConnect.h"
#include "AccelSensor.h"

int16_t ax_list[10001];
int16_t ay_list[10001];
int16_t az_list[10001];

AccelSensor accel;
int i, j;

// Serial and Accelerometer sensor configuration
void setup() {
  Serial.begin(115200);
  accel.setConfig();


}
void loop() {

  for(j=0;j<10;j++){

    // Store 10.000 sensor data in the buffer
    for(i=0; i < 10001; i++){
      accel.getEvent();
      ax_list[i] = accel.ax;
      ay_list[i] = accel.ay;
      az_list[i] = accel.az;

    }

    // Send all buffer by serial communication
    for( i=0; i < 10001; i++){
      Serial.println(String(ax_list[i]) +","+ String(ay_list[i]) +","+ String(az_list[i]));

    }
  }
  // Lock the ESP32 in an infinite loop to stop its execution
  while(1){}
  
}