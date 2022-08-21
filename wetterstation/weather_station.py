import RPi.GPIO as GPIO

from input.temperature_sensor import TemperatureSensor
from ui.ui import UI

class WeatherStation:
    def __init__(self, temperature_sensor, humidity_sensor, brightness_sensor):
        self.__temperature_sensor = temperature_sensor
        self.__humidity_sensor = humidity_sensor
        self.__brightness_sensor = brightness_sensor

        self.__user_interfaces = []

        self.__converted_temperature_unit = TemperatureSensor.CELSIUS

    def add_ui(self, ui: UI):
        self.__user_interfaces.append(ui)

    def remove_ui(self, ui: UI):
        ui.disable()
        self.__user_interfaces.remove(ui)

    def is_registered(self, ui: UI):
        return ui in self.__user_interfaces

    def loop(self):
        # Sensorwerte einlesen
        self.__read_sensors()

        # Benutzeroberflächen aktualisieren
        for ui in self.__user_interfaces:
            ui.loop()

    def __read_sensors(self):
        self.__temperature_sensor.read()
        self.celsius_temperature = self.__temperature_sensor.get_temperature_in_unit(TemperatureSensor.CELSIUS)
        self.converted_temperature = self.__temperature_sensor.get_temperature_in_unit(self.__converted_temperature_unit)
        self.humidity = self.__humidity_sensor.read()
        self.brightness = self.__brightness_sensor.read()

    @property
    def converted_temperature_unit(self):
        return self.__converted_temperature_unit

    @converted_temperature_unit.setter
    def converted_temperature_unit(self, value):
        self.__converted_temperature_unit = value

        # Temperaturwert an die neue Einheit anpassen
        self.converted_temperature = self.__temperature_sensor.get_temperature_in_unit(self.__converted_temperature_unit)

    def cleanup(self):
        # Benutzeroberflächen abschalten
        for ui in self.__user_interfaces:
            ui.disable()

        GPIO.cleanup()