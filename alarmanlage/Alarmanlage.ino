#include "Sensor.h"
#include "IRSensor.h"
#include "ReedSensor.h"
#include "MQTTConnection.h"

// Piezo-Alarm
const uint8_t piezoPin = D1;

uint32_t alarmEnd = 0;

// Einbruchssensoren
const uint8_t irSensorPin = A0;
const uint16_t irDetectionThreshold = 800;
IRSensor irSensor("ir_sensor", irSensorPin, irDetectionThreshold);

const uint8_t reedSensorPin = D2;
ReedSensor reedSensor("reed_switch_1", reedSensorPin);

Sensor *sensors[] = { &irSensor, &reedSensor };

// Ein/Aus-Status
const uint8_t statusLedPin = D7;

bool sensorsEnabled = false;

// WLAN/MQTT
const char *ssid = "ssid_placeholder";
const char *password = "password_palceholder";

const char *mqttBrokerIP = "ip_address_placeholder";
const uint16_t mqttBrokerPort = 1883;
const char *mqttClientName = "esp_alarm";

MQTTConnection connection(ssid, password, mqttBrokerIP, mqttBrokerPort, mqttClientName);

void setup() {
  Serial.begin(9600);

  pinMode(piezoPin, OUTPUT);
  pinMode(statusLedPin, OUTPUT);

  connection.setup(onMessageReceived);
  connection.subscribeMQTT("esp_alarm/input/enable");
}

void loop() {
  connection.loop();

  if (sensorsEnabled) {
    for (auto &sensor : sensors) {
      if (sensor->newIntruderDetected()) {
        Serial.print("Triggering alarm from ");
        Serial.print(sensor->getName());
        Serial.println("!");

        // MQTT-Nachricht versenden
        String topic(mqttClientName);
        topic.concat("/output/");
        topic.concat(sensor->getName());
        connection.publishMQTT(topic.c_str(), "alarm");

        // 1 Sekunde Alarm
        alarmEnd = millis() + 1000;
      }
    }

    digitalWrite(statusLedPin, HIGH);
  } else {
    digitalWrite(statusLedPin, LOW);
  }

  if (alarmEnd > millis()) {
    digitalWrite(piezoPin, HIGH);
  } else {
    digitalWrite(piezoPin, LOW);
  }
}

void onMessageReceived(char *topic, unsigned char *payload, unsigned int length) {
   Serial.println("Received MQTT message.");

   if (strcmp(topic, "esp_alarm/input/enable") == 0) {
      if (payload[0] == '1' && !sensorsEnabled) {
        sensorsEnabled = true;
        connection.publishMQTT("esp_alarm/output/enabled", "1");
        Serial.println("Enabled alarm.");
      } else if (payload[0] == '0' && sensorsEnabled) {
        sensorsEnabled = false;
        connection.publishMQTT("esp_alarm/output/enabled", "0");
        Serial.println("Disabled alarm.");
      }
   }
}
