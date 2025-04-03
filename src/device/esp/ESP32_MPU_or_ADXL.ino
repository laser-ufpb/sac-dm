#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_ADXL345_U.h>
#include <freertos/FreeRTOS.h>
#include <freertos/semphr.h>

// Configuração geral
#define BUFFER_SIZE 10000

// Objetos do acelerômetro
Adafruit_MPU6050 accelMPU;
Adafruit_ADXL345_Unified accelADXL = Adafruit_ADXL345_Unified(12345);

// Buffer circular
volatile float accelDataX[BUFFER_SIZE] = {0.0};
volatile float accelDataY[BUFFER_SIZE] = {0.0};
volatile float accelDataZ[BUFFER_SIZE] = {0.0};

// Índices do buffer
volatile int readIndex = 0;
volatile int writeIndex = 0;

// Semáforos de controle
SemaphoreHandle_t freeSpaceSemaphore;         // Espaços livres no buffer
SemaphoreHandle_t bufferHasDataSemaphore;     // Dados disponíveis para leitura
portMUX_TYPE mux = portMUX_INITIALIZER_UNLOCKED;

// Controle do sensor usado
String acc = "";

// Flag para ativar/desativar o contador de leituras por segundo
bool enableRateMonitor = true;

void task1(void *pvParameters) {
  (void)pvParameters;
  sensors_event_t event, g, temp;

  while (1) {
    // Leitura do acelerômetro
    if (acc == "MPU") {
      accelMPU.getEvent(&event, &g, &temp);
    } else {
      accelADXL.getEvent(&event);
    }

    // Espera até haver espaço livre no buffer
    xSemaphoreTake(freeSpaceSemaphore, portMAX_DELAY);

    // Escreve no buffer com proteção
    portENTER_CRITICAL(&mux);
    accelDataX[writeIndex] = event.acceleration.x;
    accelDataY[writeIndex] = event.acceleration.y;
    accelDataZ[writeIndex] = event.acceleration.z;
    writeIndex = (writeIndex + 1) % BUFFER_SIZE;
    portEXIT_CRITICAL(&mux);

    // Sinaliza que há dado disponível para leitura
    xSemaphoreGive(bufferHasDataSemaphore);

    delay(10); // Intervalo entre leituras
  }
}

void task2(void *pvParameters) {
  (void)pvParameters;
  char cMsg[254];
  int delayTime = (acc == "ADXL") ? 160 : 320;

  // Variáveis do contador de leituras por segundo
  unsigned long lastTime = millis();
  int readCount = 0;

  while (1) {
    // Espera até haver dado no buffer
    xSemaphoreTake(bufferHasDataSemaphore, portMAX_DELAY);

    float x, y, z;

    // Lê do buffer com proteção
    portENTER_CRITICAL(&mux);
    x = accelDataX[readIndex];
    y = accelDataY[readIndex];
    z = accelDataZ[readIndex];
    readIndex = (readIndex + 1) % BUFFER_SIZE;
    portEXIT_CRITICAL(&mux);

    // Sinaliza que há um espaço livre no buffer
    xSemaphoreGive(freeSpaceSemaphore);

    // Exibe os dados na serial
    sprintf(cMsg, "%0.2f;%0.2f;%0.2f", x, y, z);
    Serial.println(cMsg);

    // Contador de leituras por segundo
    if (enableRateMonitor) {
      readCount++;
      if (millis() - lastTime >= 1000) {
        Serial.print("Leituras por segundo: ");
        Serial.println(readCount);
        readCount = 0;
        lastTime = millis();
      }
    }

    delayMicroseconds(delayTime);
  }
}

void setup() {
  Serial.begin(921600);
  delay(1000);
  Serial.println("Testando inicio");

  // Inicializa acelerômetro
  if (!accelMPU.begin()) {
    Serial.println("Falha ao iniciar o MPU6050!");
    if (!accelADXL.begin()) {
      Serial.println("Falha ao iniciar o ADXL345!");
      while (1) {
        Serial.println("Falha ao iniciar os dois!");
        delay(1000);
      }
    } else {
      acc = "ADXL";
    }
  } else {
    acc = "MPU";
  }

  delay(500);
  if (acc == "MPU") {
    accelMPU.setAccelerometerRange(MPU6050_RANGE_2_G);
    accelMPU.setGyroRange(MPU6050_RANGE_500_DEG);
    accelMPU.setFilterBandwidth(MPU6050_BAND_5_HZ);
  } else {
    accelADXL.setRange(ADXL345_RANGE_2_G);
    accelADXL.setDataRate(ADXL345_DATARATE_1600_HZ);
  }

  delay(500);

  // Criação dos semáforos
  freeSpaceSemaphore = xSemaphoreCreateCounting(BUFFER_SIZE, BUFFER_SIZE); // Começa cheio de espaço
  bufferHasDataSemaphore = xSemaphoreCreateCounting(BUFFER_SIZE, 0);       // Nenhum dado no início

  // Criação das tarefas
  xTaskCreatePinnedToCore(task1, "Task1", 10000, NULL, 1, NULL, 0); // Núcleo 0
  xTaskCreatePinnedToCore(task2, "Task2", 10000, NULL, 1, NULL, 1); // Núcleo 1
}

void loop() {
  // Nada aqui — as tarefas rodam nos núcleos separadamente
}
