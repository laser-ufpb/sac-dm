#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>

const char *SSDID = "satany";
const char *PASSWORD = "mel12345";
const char *broker = "test.mosquitto.org";
const char *clientId = "ESP32Client";
const char *topic = "testEsp32";
char messages[50];

WiFiClient espClient;
PubSubClient client(espClient);

void setupWifi()
{
  Serial.println("Starting...");
  WiFi.begin(SSDID, PASSWORD);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void serverConnection()
{
  while (!client.connected())
  {
    Serial.print("Attempting MQTT connection...");
    if (client.connect(clientId))
    {
      Serial.println("connected to server: ");
      Serial.println(broker);
    }
    else
    {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup()
{
  Serial.begin(9600);
  setupWifi();
  client.setServer(broker, 1883);
}

void loop()
{
  if (!client.connected())
  {
    serverConnection();
  }
  client.loop();
  snprintf(messages, 50, "Hello from ESP32 #%ld", random(0, 100));
  Serial1.print("Sending: ");
  Serial1.println(messages);
  client.publish(topic, messages);
  delay(2000);
}