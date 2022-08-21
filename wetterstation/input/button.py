import RPi.GPIO as GPIO

class Button:
    def __init__(self, button_pin, low_active):
        self.__button_pin = button_pin

        # Eingaben werden nur verarbeitet, nachdem die Methode enabled() aufgerufen wurde
        self.__enabled = False

        # Pin konfigurieren
        GPIO.setmode(GPIO.BOARD)
        pullup = GPIO.PUD_UP if low_active else GPIO.PUD_DOWN
        GPIO.setup(self.__button_pin, GPIO.IN, pull_up_down=pullup)
        edge = GPIO.FALLING if low_active else GPIO.RISING
        GPIO.add_event_detect(self.__button_pin, edge, bouncetime=200)

    def enable(self):
        if not self.__enabled:
            self.__enabled = True
            # Tastendrücke, die im ausgeschalteten Zustand erkannt wurden, werden verworfen
            GPIO.event_detected(self.__button_pin)

    def disable(self):
        self.__enabled = False

    def is_pressed(self):
        if self.__enabled:
            return GPIO.event_detected(self.__button_pin)
        else:
            return False