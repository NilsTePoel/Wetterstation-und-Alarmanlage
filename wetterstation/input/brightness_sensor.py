from ADC0832 import ADC0832

class BrightnessSensor:
    def __init__(self, adc_clock_pin, adc_data_pin, adc_cs_pin):
        self.__adc = ADC0832(adc_clock_pin, adc_data_pin, adc_cs_pin)

    # Gibt die aktuelle Helligkeit zurück
    # (Rundung auf 2 Nachkommastellen)
    def read(self):
        adc_value = self.__adc.read_channel(0) # 8-Bit-Auflösung

        # Umrechnung vom 8-Bit-ADC-Wert (0-255) in einen Prozentwert (0-100)
        brightness = adc_value / 255 * 100

        return round(brightness, 2)