#include "WifiConnect.h"
#include "AccelSensor.h"

WifiConnect wifi;
AccelSensor accel;

char *ssid = "brisa-2261695";
char *password = "f2qovena";
char *broker_mqtt = "broker.hivemq.com";
int broker_port = 1883;
char *topic = "/tassany";

void setup()
{
    Serial.begin(115200);
    wifi.WifiSetup(ssid, password);
    // accel.setConfig();
    wifi.MqttSetup(broker_mqtt, broker_port);
    wifi.ConnectMqtt(topic);
    // wifi.HttpRegister();
}

void loop()
{

    // accel.getEvent();
    // wifi.HttpPostAccel(String(accel.a.acceleration.x), String(accel.a.acceleration.y), String(accel.a.acceleration.z));
    wifi.Reconnect(topic);
    wifi.MqttPublish(topic, "Testando.\n");
    wifi.MqttLoop();
}
