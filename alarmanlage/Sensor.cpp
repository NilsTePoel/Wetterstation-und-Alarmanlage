#include "Sensor.h"

Sensor::Sensor(const char *name) : m_name(name), m_intruderPresent(false) {
}

bool Sensor::newIntruderDetected() {
  if (intruderDetected()) {
    if (!m_intruderPresent) {
      // Neuer Einbrecher entdeckt
      m_intruderPresent = true;
      return true;
    } else {
      // Einbrecher entdeckt, der aber schon gemeldet wurde
      return false;
    }
  } else {
    // Kein Einbrecher mehr entdeckt
    m_intruderPresent = false;
    return false;
  }
}

const char *Sensor::getName() const {
  return m_name;
}
