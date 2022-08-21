import RPi.GPIO as GPIO
import time
import math

# Quelle: https://adeept.com/video/static1/itemsfile/Adeept_Sensor_Kit_for_RPi.zip
# Code wurde an die Objektorientierung angepasst
class LEDBar:
    __CMD_MODE = 0x0000 # 8-Bit-Modus
    __ON = 0x00ff
    __OFF = 0x0000

    def __init__(self, data_pin, clock_pin):
        self.__data_pin = data_pin
        self.__clock_pin = clock_pin

        self.__clock_flag = False

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.__data_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.__clock_pin, GPIO.OUT, initial=GPIO.LOW)

    def __send_16_bit_data(self, data):
        for i in range(0, 16):
            if data & 0x8000:
                GPIO.output(self.__data_pin, GPIO.HIGH)
            else:
                GPIO.output(self.__data_pin, GPIO.LOW)

            if self.__clock_flag:
                GPIO.output(self.__clock_pin, GPIO.LOW)
                self.__clock_flag = False
            else:
                GPIO.output(self.__clock_pin, GPIO.HIGH)
                self.__clock_flag = True
            time.sleep(0.001)
            data = data << 1

    def __latch_data(self):
        latch_flag = False
        GPIO.output(self.__data_pin, GPIO.LOW)
        time.sleep(0.05)

        for i in range(0, 8):
            if latch_flag:
                GPIO.output(self.__data_pin, GPIO.LOW)
                latch_flag = False
            else:
                GPIO.output(self.__data_pin, GPIO.HIGH)
                latch_flag = True
        time.sleep(0.05)

    def __send_led(self, led_state):
        for i in range(0, 12):
            if (led_state & 0x0001):
                self.__send_16_bit_data(LEDBar.__ON)
            else:
                self.__send_16_bit_data(LEDBar.__OFF)
            led_state = led_state >> 1

    def show_number(self, number):
        self.__send_16_bit_data(LEDBar.__CMD_MODE)
        self.__send_led(number)
        self.__latch_data()

    def show_percentage(self, percent):
        enabled_segments = int(percent / 10)
        led_state = int(math.pow(2, enabled_segments) - 1)
        self.show_number(led_state)