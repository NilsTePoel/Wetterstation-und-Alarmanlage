import Adafruit_DHT

class HumiditySensor:
    def __init__(self, sensor_pin, sensor_type=Adafruit_DHT.DHT22):
        self.__sensor_pin = sensor_pin
        self.__sensor_type = sensor_type

    # Gibt die aktuelle Luftfeuchtigkeit zurück
    # (Rundung auf 2 Nachkommastellen)
    def read(self):
        humidity = None

        # Sensor so lange auslesen, bis ein gültiger Wert zurückgegeben wurde
        while humidity is None:
            # Temperatur wird hier nicht benötigt, daher ignorieren
            humidity, temperature = Adafruit_DHT.read_retry(self.__sensor_type, self.__sensor_pin)

        # Die Luftfeuchtigkeit auf einen Bereich von 0 bis 100 % beschränken
        # (evtl. notwendig, wenn der Sensor falsche Werte zurückgibt)
        humidity = max(0, min(humidity, 100))

        return round(humidity, 2)