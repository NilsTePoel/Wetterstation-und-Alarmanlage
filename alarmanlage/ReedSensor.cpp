#include "ReedSensor.h"

ReedSensor::ReedSensor(const char *name, const uint8_t reedSensorPin) :
  Sensor(name), m_reedSensorPin(reedSensorPin) {
  pinMode(m_reedSensorPin, INPUT_PULLUP);
}

bool ReedSensor::intruderDetected() {
  return digitalRead(m_reedSensorPin) == HIGH;
}
