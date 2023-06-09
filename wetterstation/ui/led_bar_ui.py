from ui.ui import UI

class LEDBarUI(UI):
    __BRIGHTNESS = 0
    __HUMIDITY = 1
    __CELSIUS_TEMPERATURE = 2

    def __init__(self, weather_station, led_bar, bar_mode_button):
        self.__led_bar = led_bar

        self.__led_bar_mode = LEDBarUI.__BRIGHTNESS

        self.__bar_mode_button = bar_mode_button
        
        self.disable()

        UI.__init__(self, weather_station)

    def loop(self):
        if self.__handle_bar_mode_button_press():
            # Beim Drücken den jetzt eingestellten Modus bis zum nächsten Durchlauf anzeigen
            self.__display_mode_on_led_bar()
        else:
            self.__display_values_on_led_bar()

    # Rückgabewert: True, falls der Knopf gedrückt wurde
    def __handle_bar_mode_button_press(self):
        # Taste wenn nötig freischalten
        self.__bar_mode_button.enable()

        if self.__bar_mode_button.is_pressed():
            # Anzeige auf dem LED-Streifen ändern
            self.__led_bar_mode = (self.__led_bar_mode + 1) % 3
            return True
        else:
            return False

    def __display_mode_on_led_bar(self):
        # Helligkeit: 1 Balken am oberen Ende des LED-Anzeige ist hell
        # Luftfeuchtigkeit: 2 Balken am oberen Ende des LED-Anzeige sind hell
        # Temperatur: 3 Balken am oberen Ende des LED-Anzeige sind hell
        mode_number = 0b111 << (10 - (self.__led_bar_mode + 1))
        self.__led_bar.show_number(mode_number)

    def __display_values_on_led_bar(self):
        if self.__led_bar_mode == LEDBarUI.__BRIGHTNESS:
            self.__led_bar.show_percentage(self._weather_station.brightness)
        elif self.__led_bar_mode == LEDBarUI.__HUMIDITY:
            self.__led_bar.show_percentage(self._weather_station.humidity)
        elif self.__led_bar_mode == LEDBarUI.__CELSIUS_TEMPERATURE:
            # Skalierung, damit die LED-Anzeige bei "gewöhnlichen" Raumtemperaturen besser ausgenutzt wird
            scale_factor = 2
            self.__led_bar.show_percentage(self._weather_station.celsius_temperature * scale_factor)

    def disable(self):
        # Anzeige ausschalten
        self.__led_bar.show_percentage(0)

        # Taste sperren
        self.__bar_mode_button.disable()