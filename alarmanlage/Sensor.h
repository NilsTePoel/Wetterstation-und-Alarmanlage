#pragma once

class Sensor {
public:
  Sensor(const char *name);

  bool newIntruderDetected();

  const char *getName() const;

private:
  const char *m_name;

  bool m_intruderPresent;

  virtual bool intruderDetected() = 0;
};
