#pragma once

#include <Arduino.h>

#include "Sensor.h"

class ReedSensor : public Sensor {
public:
  ReedSensor(const char *name, const uint8_t reedSensorPin);

private:
  const uint8_t m_reedSensorPin;

  bool intruderDetected();
};
