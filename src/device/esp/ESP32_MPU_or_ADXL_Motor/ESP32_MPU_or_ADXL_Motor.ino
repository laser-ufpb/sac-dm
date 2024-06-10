#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_ADXL345_U.h>
#include <ESP32Servo.h>

#define ESCPin 17
#define USE_SERIAL Serial

Servo ServoMotor;
int potServor=0;
 
String acc = "";
 
volatile int line = 0;
 
// Objetos do acelerômetro
Adafruit_MPU6050 accelMPU;
Adafruit_ADXL345_Unified accelADXL = Adafruit_ADXL345_Unified(12345);
 
// Mutex para garantir acesso exclusivo às variáveis compartilhadas
portMUX_TYPE mux = portMUX_INITIALIZER_UNLOCKED;
 
/* Objeto do servo Motor */


// Variáveis compartilhadas entre os núcleos
volatile float accelDataX = 0.0;
volatile float accelDataY = 0.0;
volatile float accelDataZ = 0.0;
 
void task1(void *pvParameters) {
  (void)pvParameters;
 
  sensors_event_t event, g, temp;
 
  while (1) {
    // Leitura dos dados do acelerômetro
    if(acc == "MPU"){
      accelMPU.getEvent(&event, &g, &temp);
    } else{
      accelADXL.getEvent(&event);
    }
 
    // Aquisição do mutex para garantir acesso exclusivo às variáveis compartilhadas
    portENTER_CRITICAL(&mux);
    accelDataX = event.acceleration.x;
    accelDataY = event.acceleration.y;
    accelDataZ = event.acceleration.z;
    portEXIT_CRITICAL(&mux);

    if(USE_SERIAL.available() > 0) {
      potServor = USE_SERIAL.parseInt();
      ServoMotor.write(potServor);
    }
 
  }
}
 
void task2(void *pvParameters) {
  (void)pvParameters;
  char cMsg[254];
  line++;
  int delay = 320;
 
  if(acc == "ADXL"){
    delay = 160;
  } 
 
  while (1) {
    // Aquisição do mutex para garantir acesso exclusivo às variáveis compartilhadas
    portENTER_CRITICAL(&mux);
    float x = accelDataX;
    float y = accelDataY;
    float z = accelDataZ;
 
    portEXIT_CRITICAL(&mux);
 
    sprintf(cMsg, "%0.2f;%0.2f;%0.2f", x, y, z );
    //sprintf(cMsg, "%0.2f;%0.2f;%0.2f", x, y, z);
    Serial.println(cMsg);
    delayMicroseconds(delay);
  }
}
 
 
void setup() {
  Serial.begin(921600);
  //Serial.begin(230400);  
  delay(1000);
  // Inicialização do acelerômetro
  Serial.println("Testando inicio");
 
    if (!accelMPU.begin()) {
      Serial.println("Falha ao iniciar o MPU6050!");
 
      if (!accelADXL.begin()) {
        Serial.println("Falha ao iniciar o ADXL345!");
        while (1){
          Serial.println("Falha ao iniciar os dois!");
          delay(1000);
        }
      }
      else {
        acc = "ADXL";
      }
 
    } else {
      acc = "MPU";
    }
  delay(500); 
  if(acc == "MPU"){
    accelMPU.setAccelerometerRange(MPU6050_RANGE_2_G);
    accelMPU.setGyroRange(MPU6050_RANGE_500_DEG);
    accelMPU.setFilterBandwidth(MPU6050_BAND_5_HZ);
  } else { 
    accelADXL.setRange(ADXL345_RANGE_2_G);
    accelADXL.setDataRate(ADXL345_DATARATE_1600_HZ);
  }
  delay(500);

  //  Servor 
  ServoMotor.attach(ESCPin);

  while (USE_SERIAL.available() <= 0) {
    delay(1000); 
    ServoMotor.write(0); 
    USE_SERIAL.println("Aguardando potência:");        
  }
  
  potServor = USE_SERIAL.parseInt();

  USE_SERIAL.println("Turning engine on ...");
  ServoMotor.write(0);  delay(10000);
  ServoMotor.write(20); delay(2000);
  ServoMotor.write(0);  delay(5000); 
  ServoMotor.write(potServor);

 
  // Criação das tasks
  xTaskCreatePinnedToCore(task1, "Task1", 10000, NULL, 1, NULL, 0); // Task 1 no núcleo 0
  xTaskCreatePinnedToCore(task2, "Task2", 10000, NULL, 1, NULL, 1); // Task 2 no núcleo 1
}
 
void loop() {
  // O loop principal é deixado vazio, já que as tasks estão sendo executadas nos núcleos separados
}