# Wetterstation und Alarmanlage

## Wetterstation

### Funktionen

Die Wetterstation läuft auf einem Raspberry Pi und misst die aktuelle Temperatur, Luftfeuchtigkeit und Helligkeit.

An die Wetterstation sind zwei lokale Anzeigen angeschlossen: ein LCD, das die aktuellen Messwerte anzeigt und ein LED-Streifen, der jeweils eine der drei Messgrößen grafisch darstellt. Mit zwei Tasten kann die Temperatureinheit auf dem LCD und die auf der LED-Anzeige dargestellte Messgröße angepasst werden.

Zusätzlich werden die Messdaten über das MQTT-Protokoll an ein [Node-RED-Dashboard](#node-red-dashboard) gesendet.

### Aufbau

Die Pin-Belegung und andere Hardware-Einstellungen (z. B. die I²C-Adresse des LCD) können über die Konstanten in der Datei `__main__.py` (Abschnitt "Peripherie") geändert werden.

Es wird die physikalische Nummerierung der Pins genutzt. I²C und die 1-Wire-Schnittstelle müssen in den Raspberry Pi-Einstellungen aktiviert werden.

| Bauteil                                            | Pin-Belegung                     |
| -------------------------------------------------- | -------------------------------- |
| LCD1602 mit I²C                                    | SDA, SCL                         |
| [LED-Anzeige](https://www.adeept.com/adeept-new-10-segment-led-bar-graph-module-for-arduino-raspberry-pi-arm-avr-dsp-pic-freeshipping-headphones-diy-diykit_p0065.html) | 38 (Data), 40 (Clock) |
| Taste zum Ändern der Temperatureinheit             | 16                               |
| Taste zum Ändern der Messgröße auf der LED-Anzeige | 35                               |
| Temperatursensor DS18B20                           | 7                                |
| Luftfeuchtigkeitssensor DHT22                      | 26                               |
| Analog-Digital-Converter ADC0832                   | 11 (CS), 12 (Data), 13 (Clock)   |
| Fotowiderstand                                     | Angeschlossen an Kanal 0 des ADC |

### Verwendete Bibliotheken

* [RPLCD](https://github.com/dbrgn/RPLCD)
* [Adafruit DHT Sensor Library](https://github.com/adafruit/Adafruit_Python_DHT)
* [RasPyADC0832](https://github.com/InvncibiltyCloak/RasPyADC0832/)
* [Paho MQTT Client](https://github.com/eclipse/paho.mqtt.python)

## Alarmanlage

## Node-RED-Dashboard
