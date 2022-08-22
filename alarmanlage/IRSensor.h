#pragma once

#include <Arduino.h>

#include "Sensor.h"

class IRSensor : public Sensor {
public:
  IRSensor(const char *name, const uint8_t irSensorPin, const uint16_t irDetectionThreshold);

private:
  const uint8_t m_irSensorPin;
  const uint16_t m_irDetectionThreshold;

  bool intruderDetected();
};
