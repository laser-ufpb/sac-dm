#include "AccelSensor.h"

AccelSensor::AccelSensor()
{
}

void AccelSensor::getEvent()
{

    mpu.getEvent(&a, &g, &temp);
}
void AccelSensor::setConfig()
{

    if (!mpu.begin())
    {
        // Serial.println("Failed to find MPU6050 chip");
        while (1)
        {
            delay(10);
        }
    }
    // Serial.println("MPU6050 Found!");

    mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
    mpu.setGyroRange(MPU6050_RANGE_500_DEG);
    mpu.setFilterBandwidth(MPU6050_BAND_5_HZ);

    delay(100);
}

char* AccelSensor::dataOutput(float AcclX, float AcclY, float AcclZ)
{
  
    std::string data = "Aceleração nos vetores: X = ";
  
    // data += std::to_string(AcclX);
    // data += " Y = ";
    // data += std::to_string(AcclY);
    // data += " Z = ";
    // data += std::to_string(AcclZ);
    char aux[data.size()];

    strcat(aux,data.c_str());
    return aux;
}
