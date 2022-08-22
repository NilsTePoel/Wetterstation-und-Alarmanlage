#include "MQTTConnection.h"

MQTTConnection::MQTTConnection(const char *ssid, const char *password, const char* mqttBrokerIP, const uint16_t mqttBrokerPort, const char* mqttClientName) :
  m_ssid(ssid), m_password(password), m_mqttBrokerIP(mqttBrokerIP), m_mqttBrokerPort(mqttBrokerPort), m_mqttClientName(mqttClientName), m_mqttClient(m_wiFiClient) {
}

void MQTTConnection::setup(void (*callback)(char*, unsigned char*, unsigned int)) {
  WiFi.begin(m_ssid, m_password);

  Serial.println("Connecting to WiFi ...");

  // Warten, bis die Verbindung aufgebaut ist
  while (WiFi.status() != WL_CONNECTED){
    // delay() setzt den Watchdog-Timer zurück
    delay(100);
  }

  // IP-Adresse ausgeben
  Serial.print("WiFi connected. IP address: ");
  Serial.println(WiFi.localIP());

  // MQTT konfigurieren und verbinden
  m_mqttClient.setServer(m_mqttBrokerIP, m_mqttBrokerPort);
  m_mqttClient.setCallback(callback);
  m_mqttClient.connect(m_mqttClientName);

  Serial.println("MQTT connected.");
}

void MQTTConnection::loop() {
  if (WiFi.status() != WL_CONNECTED) {
    reconnectWiFi();
  }

  if (!m_mqttClient.connected()) {
    reconnectMQTT();
  } else {
    m_mqttClient.loop();
  }
}

void MQTTConnection::publishMQTT(const char *topic, const char *value) {
  m_mqttClient.publish(topic, value);
}

void MQTTConnection::subscribeMQTT(const char *topic) {
  m_mqttClient.subscribe(topic);
}

void MQTTConnection::reconnectWiFi() {
  Serial.println("WiFi connection lost. Reconnecting ...");

  // Neu verbinden
  WiFi.disconnect();
  WiFi.mode(WIFI_OFF);
  WiFi.mode(WIFI_STA);
  WiFi.begin(m_ssid, m_password);

  // Warten, bis die Verbindung wieder aufgebaut ist
  while (WiFi.status() != WL_CONNECTED) {
    // delay() setzt den Watchdog-Timer zurück
    delay(100);
  }

  Serial.println("WiFi reconnected");
}

void MQTTConnection::reconnectMQTT() {
  Serial.println("MQTT connection lost. Reconnecting ...");

  // Neuverbindung so lange wiederholen, bis sie erfolgreich war
  while (!m_mqttClient.connected()) {
    if (m_mqttClient.connect(m_mqttClientName)) {
      Serial.println("MQTT connected.");
    } else {
      Serial.println("MQTT reconnection failed. Trying again ...");
      delay(1000);
    }
  }
}
