#include "IRSensor.h"

IRSensor::IRSensor(const char *name, const uint8_t irSensorPin, const uint16_t irDetectionThreshold) :
  Sensor(name), m_irSensorPin(irSensorPin), m_irDetectionThreshold(irDetectionThreshold) {
}

bool IRSensor::intruderDetected() {
  uint16_t distance = analogRead(m_irSensorPin);

  // Kurze Wartezeit, damit die WLAN-Verbindung nicht abbricht
  delay(3);

  return distance < m_irDetectionThreshold;
}
