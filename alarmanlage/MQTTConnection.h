#pragma once

#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// Baut eine MQTT-Verbindung auf und übernimmt die Fehlerbehandlung (-> Neuverbindung bei Verbindungsabbruch)
class MQTTConnection {
public:
  MQTTConnection(const char *ssid, const char *password, const char *mqttBrokerIP, const uint16_t mqttBrokerPort, const char *mqttClientName);

  void setup(void (*callback)(char*, unsigned char*, unsigned int));

  // Übernimmt eventuell notwendige Neuverbindungen
  void loop();

  void publishMQTT(const char *topic, const char *value);
  void subscribeMQTT(const char *topic);

private:
  const char *m_ssid;
  const char *m_password;
  const char *m_mqttBrokerIP;
  const uint16_t m_mqttBrokerPort;
  const char *m_mqttClientName;

  WiFiClient m_wiFiClient;
  PubSubClient m_mqttClient;

  void reconnectWiFi();
  void reconnectMQTT();
};
