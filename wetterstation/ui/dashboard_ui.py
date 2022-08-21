from ui.ui import UI

class DashboardUI(UI):
    def __init__(self, weather_station, mqtt_client, mqtt_client_name):
        self.__mqtt_client = mqtt_client
        self.__mqtt_client_name = mqtt_client_name

        UI.__init__(self, weather_station)

    def loop(self):
        self.__publish_data()

    def __publish_data(self):
        self.__mqtt_client.publish(self.__get_topic("temperature"), self._weather_station.celsius_temperature)
        self.__mqtt_client.publish(self.__get_topic("humidity"), self._weather_station.humidity)
        self.__mqtt_client.publish(self.__get_topic("brightness"), self._weather_station.brightness)

    def __get_topic(self, unit):
        return self.__mqtt_client_name + "/output/" + unit