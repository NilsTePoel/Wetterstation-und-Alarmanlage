class TemperatureSensor:
    CELSIUS = 0
    KELVIN = 1
    FAHRENHEIT = 2

    def __init__(self, sensor_id):
        self.__sensor_id = sensor_id

    # Liest einen neuen Temperaturwert ein
    # Aufrufen, bevor die Temperatur mit get_temperature_in_unit() abgefragt wird
    def read(self):
        # Zugriff auf Sensor erfolgt über das 1-Wire-Protokoll
        file_name = "/sys/bus/w1/devices/" + self.__sensor_id + "/w1_slave"
        file = open(file_name)
        sensor_input = file.read()
        file.close()

        # Eingelesene Daten bis zum Anfang des Temperaturwerts abschneiden
        temperature_data = sensor_input.split("t=")[1]

        # Temperaturwert in die korrekte Einheit bringen
        self.__celsius_temperature = float(temperature_data) / 1000

    # Gibt den zuletzt eingelesenen Temperaturwert in der angegebenen Einheit zurück
    # (Rundung auf 2 Nachkommastellen)
    def get_temperature_in_unit(self, temperature_unit):
        temperature = self.__celsius_temperature

        if temperature_unit == TemperatureSensor.KELVIN:
            temperature += 273.15
        elif temperature_unit == TemperatureSensor.FAHRENHEIT:
            temperature = (temperature * (9 / 5)) + 32

        return round(temperature, 2)