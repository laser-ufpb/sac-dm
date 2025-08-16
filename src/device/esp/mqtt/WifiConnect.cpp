#include <Arduino.h>
#include "WifiConnect.h"
WiFiClient espClient;
PubSubClient MQTT(espClient);

void mqtt_callback(char *topic, byte *payload, unsigned int length)
{
    Serial.print("Mensagem [");
    Serial.print(topic);
    Serial.print("] ");
    for (int i = 0; i < length; i++)
    {
        Serial.print((char)payload[i]);
    }
    Serial.println();
}

WifiConnect::WifiConnect()
{
}
void WifiConnect::Reconnect(char *topic)
{
    if (!MQTT.connected())
    {
      while (!MQTT.connected()) {
        Serial.println("Attempting MQTT connection...");
        if (MQTT.connect("ESP32_clientID")) {
          Serial.println("connected");
          // Once connected, publish an announcement...
          MQTT.publish("/tassany", "Nodemcu connected to MQTT");
          // ... and resubscribe
          MQTT.subscribe("/tassany");

        } else {
          Serial.print("failed, rc=");
          Serial.print(MQTT.state());
          Serial.println(" try again in 5 seconds");
          // Wait 5 seconds before retrying
          delay(5000);
        }
      }
    }
}

void WifiConnect::ConnectMqtt(char *topic)
{
    MQTT.connect("ESP32_clientID"); // ESP will connect to mqtt broker with clientID
    {
        Serial.println("connected to MQTT");
        // Once connected, publish an announcement...

        // ... and resubscribe
        MQTT.subscribe(topic); // topic=Demo
        MQTT.publish(topic, "connected to MQTT");

        if (!MQTT.connected())
        {
            Reconnect(topic);
        }
    }
}

void WifiConnect::WifiSetup(char *ssid, char *password)
{

    WiFi.begin(ssid, password);
    Serial.println("Connecting");
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }
    Serial.println("");
    Serial.print("Connected to WiFi network with IP Address: ");
    Serial.println(WiFi.localIP());
}
// void WifiConnect::HttpRegister()
// {

//     const char *server_name = "https://enmpf6xid68v.x.pipedream.net/";

//     if (WiFi.status() == WL_CONNECTED)
//     {

//         HTTPClient http;

//         http.begin(server_name);

//         http.addHeader("Content-Type", "application/json");

//         int httpResponseCode = http.POST("{\"mac_adress\":\"" + WiFi.macAddress() + "\",\"device_type\":\"esp32\"}");

//         Serial.print("HTTP Response code: ");
//         Serial.println(httpResponseCode);

//         http.end();
//     }
//     else
//         Serial.println("Wifi Disconnected");
// }
// void WifiConnect::HttpPostAccel(String AcclX, String AcclY, String AcclZ)
// {

//     // https://enmpf6xid68v.x.pipedream.net/
//     // https://test-implantacao.rj.r.appspot.com/accelerometer

//     const char *server_name = "https://enmpf6xid68v.x.pipedream.net/";

//     if (WiFi.status() == WL_CONNECTED)
//     {

//         Serial.begin(115200);

//         HTTPClient http;

//         http.begin(server_name);

//         http.addHeader("Content-Type", "application/json");

//         String data;

//         data = "{\"device_code\":\"01\",\"ACx\":\"" + AcclX + "\",\"ACy\":\"" + AcclY + " \",\"ACz\":\"" + AcclZ + "\"}";

//         int httpResponseCode = http.POST(data);

//         Serial.print("HTTP Response code: ");
//         Serial.println(httpResponseCode);

//         http.end();
//     }
//     else
//         Serial.println("Wifi Disconnected");
// }
void WifiConnect::MqttSetup(char *broker_mqtt, int broker_port)
{
    MQTT.setServer(broker_mqtt, broker_port); // connecting to mqtt server
    MQTT.setCallback(mqtt_callback);
}

void WifiConnect::MqttPublish(char *broker_topic, String data)
{
    const char *pub = data.c_str();
    MQTT.publish(broker_topic, pub);
    
}

void WifiConnect::MqttLoop()
{
    MQTT.loop();
}
