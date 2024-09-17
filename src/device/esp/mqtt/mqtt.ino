#include "WifiConnect.h"
#include "AccelSensor.h"

WifiConnect wifi;
AccelSensor accel;

char *ssid = "Lieno";
char *password = "ijta1920";
char *broker_mqtt = "broker.hivemq.com";
int broker_port = 1883;
char *topic = "/aviacao";

void setup()
{
    Serial.begin(115200);
    wifi.WifiSetup(ssid, password);
    accel.setConfig();
    wifi.MqttSetup(broker_mqtt, broker_port);
    wifi.ConnectMqtt(topic);
    // wifi.HttpRegister();
}

void loop()
{


    accel.getEvent();
    Serial.println(accel.accel.a.acceleration.x);
    wifi.MqttPublish(topic, String(accel.accel.a.acceleration.x));
    delay(1000);
    wifi.MqttLoop();
}
