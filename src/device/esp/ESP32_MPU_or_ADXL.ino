#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_ADXL345_U.h>
#include <freertos/FreeRTOS.h>
#include <freertos/semphr.h>

// Configuração geral
#define ADXL345_ADDRESS 0x53
#define BUFFER_SIZE 10000
#define INIT_DELAY_MS 500
#define SERIAL_BAUDRATE 921600

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

void setupADXL_FIFO() {
  Wire.beginTransmission(ADXL345_ADDRESS);
  Wire.write(0x2D); // POWER_CTL
  Wire.write(0x08); // Measure mode
  Wire.endTransmission();

  Wire.beginTransmission(ADXL345_ADDRESS);
  Wire.write(0x31); // DATA_FORMAT
  Wire.write(0x0B); // Full resolution, +/-16g
  Wire.endTransmission();

  Wire.beginTransmission(ADXL345_ADDRESS);
  Wire.write(0x38); // FIFO_CTL
  Wire.write(0x9F); // FIFO mode = Stream (0b10), Trigger = INT1, Samples = 31
  Wire.endTransmission();
}

uint8_t getFifoSampleCount() {
  Wire.beginTransmission(ADXL345_ADDRESS);
  Wire.write(0x39); // FIFO_STATUS
  Wire.endTransmission(false);
  Wire.requestFrom(ADXL345_ADDRESS, 1);
  return Wire.read() & 0x3F; // Bits 0-5: sample count
}

void readAdxlFifoAndStoreInBuffer(uint8_t sampleCount) {
  for (int i = 0; i < sampleCount; i++) {
    // Espera por espaço no buffer circular
    xSemaphoreTake(freeSpaceSemaphore, portMAX_DELAY);

    // Leitura dos 6 bytes (X, Y, Z)
    Wire.beginTransmission(ADXL345_ADDRESS);
    Wire.write(0x32); // Início do registro de dados
    Wire.endTransmission(false);
    Wire.requestFrom(ADXL345_ADDRESS, 6);

    int16_t rawX = Wire.read() | (Wire.read() << 8);
    int16_t rawY = Wire.read() | (Wire.read() << 8);
    int16_t rawZ = Wire.read() | (Wire.read() << 8);

    // Converte para G: 4mg/LSB (full-res, ±16g)
    float x = rawX * 0.0039;
    float y = rawY * 0.0039;
    float z = rawZ * 0.0039;

    // Escreve no buffer circular com proteção
    portENTER_CRITICAL(&mux);
    accelDataX[writeIndex] = x;
    accelDataY[writeIndex] = y;
    accelDataZ[writeIndex] = z;
    writeIndex = (writeIndex + 1) % BUFFER_SIZE;
    portEXIT_CRITICAL(&mux);

    // Sinaliza que há dado disponível
    xSemaphoreGive(bufferHasDataSemaphore);
  }
}

void task1(void *pvParameters) {
  (void)pvParameters;

  while (1) {
    if (acc == "ADXL") {
      uint8_t availableSamples = getFifoSampleCount();
      if (availableSamples > 0) {
        readAdxlFifoAndStoreInBuffer(availableSamples);
      }
    } else {
      // Leitura normal do MPU6050 (caso esteja sendo usado)
      sensors_event_t event, g, temp;
      accelMPU.getEvent(&event, &g, &temp);

      xSemaphoreTake(freeSpaceSemaphore, portMAX_DELAY);
      portENTER_CRITICAL(&mux);
      accelDataX[writeIndex] = event.acceleration.x;
      accelDataY[writeIndex] = event.acceleration.y;
      accelDataZ[writeIndex] = event.acceleration.z;
      writeIndex = (writeIndex + 1) % BUFFER_SIZE;
      portEXIT_CRITICAL(&mux);
      xSemaphoreGive(bufferHasDataSemaphore);
    }

    delay(1); // Evita uso excessivo da CPU
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
  Serial.begin(SERIAL_BAUDRATE);
  delay(INIT_DELAY_MS);
  Serial.println("Testando inicio");

  // Inicializa acelerômetro
  if (!accelMPU.begin()) {
    Serial.println("Falha ao iniciar o MPU6050!");
    if (!accelADXL.begin()) {
      Serial.println("Falha ao iniciar o ADXL345!");
      while (1) {
        Serial.println("Falha ao iniciar os dois!");
        delay(INIT_DELAY_MS);
      }
    } else {
      acc = "ADXL";
      setupADXL_FIFO();
    }
  } else {
    acc = "MPU";
  }

  delay(INIT_DELAY_MS);
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
