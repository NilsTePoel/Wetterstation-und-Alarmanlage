from datetime import datetime

from ui.ui import UI

class LCDUI(UI):
    __SHOW_DATE = 0
    __SHOW_HUMIDITY = 1
    __SHOW_BRIGHTNESS = 2

    def __init__(self, weather_station, lcd, unit_button):
        self.__lcd = lcd

        self.__second_line_mode = LCDUI.__SHOW_DATE

        self.__unit_button = unit_button
        
        self.disable()

        UI.__init__(self, weather_station)

    def loop(self):
        self.__handle_unit_button_press()
        self.__display_values_on_lcd()

    def __handle_unit_button_press(self):
        # Taste wenn nötig freischalten
        self.__unit_button.enable()

        if self.__unit_button.is_pressed():
            # Temperatureinheit ändern
            new_unit = (self._weather_station.converted_temperature_unit + 1) % 3
            self._weather_station.converted_temperature_unit = new_unit

    def __display_values_on_lcd(self):
        # Hintergrundbeleuchtung könnte durch disable()-Aufruf deaktiviert sein
        self.__lcd.backlight_enabled = True

        # 1. Zeile: Temperatur
        unit_signs = ["\337C", "K", "F"]
        current_unit_sign = unit_signs[self._weather_station.converted_temperature_unit]
        formatted_temperature = "Temp.: {:.2f} {:2}".format(self._weather_station.converted_temperature, current_unit_sign)

        self.__lcd.cursor_pos = (0, 0)
        self.__lcd.write_string(formatted_temperature)

        # 2. Zeile: Wechsel zw. Datum, Luftfeuchtigkeit und Helligkeit
        self.__lcd.cursor_pos = (1, 0)
        if self.__second_line_mode == LCDUI.__SHOW_DATE:
            # Datum ausgeben
            # Format: Tag. Monat, Stunde:Minute
            self.__lcd.write_string(datetime.now().strftime("%d. %b, %H:%M  "))
        elif self.__second_line_mode == LCDUI.__SHOW_HUMIDITY:
            # Luftfeuchtigkeit ausgeben
            self.__lcd.write_string("Feuchtigk.: {:>3.0f}%".format(self._weather_station.humidity))
        elif self.__second_line_mode == LCDUI.__SHOW_BRIGHTNESS:
            # Helligkeit ausgeben
            self.__lcd.write_string("Helligk.: {:>3.0f}%  ".format(self._weather_station.brightness))

        # Im nächsten Durchlauf andere Anzeige auf der 2. LCD-Zeile
        self.__second_line_mode = (self.__second_line_mode + 1) % 3

    def disable(self):
        # LCD ausschalten
        self.__lcd.clear()
        self.__lcd.backlight_enabled = False

        # Taste sperren
        self.__unit_button.disable()