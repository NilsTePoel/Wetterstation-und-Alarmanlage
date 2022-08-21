class UI:
    def __init__(self, weather_station):
        self._weather_station = weather_station

    def loop(self):
        # Wird von den Unterklassen implementiert
        pass

    def disable(self):
        # Wird von den Unterklassen implementiert (falls erforderlich)
        pass