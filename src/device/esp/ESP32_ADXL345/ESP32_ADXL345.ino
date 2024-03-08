#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>

volatile int line = 0;

// Objeto do acelerômetro
Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(12345); // O parâmetro é um identificador exclusivo, pode ser qualquer número

// Mutex para garantir acesso exclusivo às variáveis compartilhadas
portMUX_TYPE mux = portMUX_INITIALIZER_UNLOCKED;

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

    //sprintf(cMsg, "%0.2f , %0.2f, %0.2f, %d, %d", x, y, z, millis(), line++ );
    sprintf(cMsg, "%0.2f;%0.2f;%0.2f", x, y, z);
    Serial.println(cMsg);
    delayMicroseconds(160);
  }
}

void stopClean()
{
  int i = 0;
  Serial.println("=== stopClean() ===");
  while (i == 0)
    {
      Serial.println("Waiting for a exit command...");
      delay(5000);
      if(Serial.available() > 0) {
        i = Serial.parseInt();   
        }
    }
    
}

void stop()
{
  int i = 0;
  Serial.println("=== stop() ===");
  while (i == 0)
    {
      Serial.println("Waiting for a exit command...");
      delay(5000);
      if(Serial.available() > 0) {
        i = Serial.parseInt();   
        }
    }
    
}

void setup() {
  Serial.begin(921600);
  //Serial.begin(230400);  

  // Inicialização do acelerômetro
  if (!accel.begin()) {
    Serial.println("Falha ao iniciar o ADXL345!");
    while (1);
  }

  delay(500); 
  accel.setRange(ADXL345_RANGE_2_G);
  accel.setDataRate(ADXL345_DATARATE_1600_HZ);
  delay(500); 
  // Criação das tasks
  xTaskCreatePinnedToCore(task1, "Task1", 10000, NULL, 1, NULL, 0); // Task 1 no núcleo 0
  xTaskCreatePinnedToCore(task2, "Task2", 10000, NULL, 1, NULL, 1); // Task 2 no núcleo 1
}

void loop() {
  // O loop principal é deixado vazio, já que as tasks estão sendo executadas nos núcleos separados
}
