#include <ESP32Servo.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>
#include "WiFi.h"
#include "AsyncUDP.h"
#include "ESC.h"

volatile int line = 0;

// Objeto do acelerômetro
// O parâmetro é um identificador exclusivo, pode ser qualquer número
Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(12345); 

// Mutex para garantir acesso exclusivo às variáveis compartilhadas
portMUX_TYPE mux = portMUX_INITIALIZER_UNLOCKED;

/* Objeto do servo Motor */
Servo ServoMotor;


#define ESCPin 17
#define USE_SERIAL Serial


int potServor=0;

// Variáveis compartilhadas entre os núcleos
volatile float accelDataX = 0.0;
volatile float accelDataY = 0.0;
volatile float accelDataZ = 0.0;

void task1(void *pvParameters) {
  (void)pvParameters;

  sensors_event_t event;

  while (1) {
    // Leitura dos dados do acelerômetro
    accel.getEvent(&event);

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

  while (1) {
    // Aquisição do mutex para garantir acesso exclusivo às variáveis compartilhadas
    portENTER_CRITICAL(&mux);
    float x = accelDataX;
    float y = accelDataY;
    float z = accelDataZ;
    portEXIT_CRITICAL(&mux);

    //sprintf(cMsg, "%0.2f;%0.2f;%0.2f;%d;%d", x, y, z, millis(), line++ );
    sprintf(cMsg, "%0.2f;%0.2f;%0.2f", x, y, z);
    Serial.println(cMsg);
    delayMicroseconds(160);
  }
}

void setup() {
  Serial.begin(921600);
  //Serial1.begin(115200);  

  // Inicialização do acelerômetro
  if (!accel.begin()) {
    while (1){
      Serial.println("Falha ao iniciar o ADXL345!");
      delay(1000);
    }
  }


  delay(500); 
  accel.setRange(ADXL345_RANGE_2_G);
  accel.setDataRate(ADXL345_DATARATE_1600_HZ);
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
