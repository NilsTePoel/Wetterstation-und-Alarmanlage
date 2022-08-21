#!/usr/bin/python3

import time
from RPLCD.i2c import CharLCD
from paho.mqtt.client import Client

from input.button import Button
from input.temperature_sensor import TemperatureSensor
from input.humidity_sensor import HumiditySensor
from input.brightness_sensor import BrightnessSensor

from output.led_bar import LEDBar

from weather_station import WeatherStation

from ui.lcd_ui import LCDUI
from ui.led_bar_ui import LEDBarUI
from ui.dashboard_ui import DashboardUI

# Peripherie
LCD_DRIVER_TYPE = "PCF8574"
LCD_I2C_ADDRESS = 0x27

LED_BAR_DATA_PIN = 38
LED_BAR_CLOCK_PIN = 40

UNIT_BUTTON_PIN = 16
UNIT_BUTTON_LOW_ACTIVE = True

BAR_MODE_BUTTON_PIN = 35
BAR_MODE_BUTTON_LOW_ACTIVE = False

TEMPERATURE_SENSOR_ID = "28-020491770a5d"

HUMIDITY_SENSOR_PIN = 26

ADC_CLOCK_PIN = 13
ADC_DATA_PIN = 12
ADC_CS_PIN = 11

# MQTT
MQTT_CLIENT_NAME = "rpi_weather"
MQTT_BROKER_ADDRESS = "ip_address_placeholder"
MQTT_PORT = 1883

# Schaltet die angegebene Benutzeroberfläche anhand der MQTT-Nachricht ein bzw. aus
def change_ui_state(payload, output_topic, ui):
    if payload == "0" and weather_station.is_registered(ui):
        weather_station.remove_ui(ui)
        mqtt_client.publish(MQTT_CLIENT_NAME + "/output/" + output_topic, 0)
    elif payload == "1" and not weather_station.is_registered(ui):
        weather_station.add_ui(ui)
        mqtt_client.publish(MQTT_CLIENT_NAME + "/output/" + output_topic, 1)

# Wird aufgerufen, wenn eine MQTT-Nachricht eintrifft
def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode("utf-8")

    if topic == MQTT_CLIENT_NAME + "/input/lcd_enable":
        # LCD ein- bzw. ausschalten
        change_ui_state(payload, "lcd_enabled", lcd_ui)
    elif topic == MQTT_CLIENT_NAME + "/input/bar_enable":
        # LED-Streifen ein- bzw. ausschalten
        change_ui_state(payload, "bar_enabled", led_bar_ui)

weather_station = WeatherStation(
    TemperatureSensor(TEMPERATURE_SENSOR_ID),
    HumiditySensor(HUMIDITY_SENSOR_PIN),
    BrightnessSensor(ADC_CLOCK_PIN, ADC_DATA_PIN, ADC_CS_PIN)
)

mqtt_client = Client()

lcd_ui = LCDUI(
    weather_station,
    CharLCD(LCD_DRIVER_TYPE, LCD_I2C_ADDRESS),
    Button(UNIT_BUTTON_PIN, UNIT_BUTTON_LOW_ACTIVE)
)

led_bar_ui = LEDBarUI(
    weather_station,
    LEDBar(LED_BAR_DATA_PIN, LED_BAR_CLOCK_PIN),
    Button(BAR_MODE_BUTTON_PIN, BAR_MODE_BUTTON_LOW_ACTIVE)
)

dashboard_ui = DashboardUI(
    weather_station,
    mqtt_client, MQTT_CLIENT_NAME
)

if __name__ == '__main__':
    # MQTT konfigurieren und verbinden
    mqtt_client.on_message = on_message
    mqtt_client.connect(MQTT_BROKER_ADDRESS, MQTT_PORT)
    mqtt_client.subscribe(MQTT_CLIENT_NAME + "/input/lcd_enable")
    mqtt_client.subscribe(MQTT_CLIENT_NAME + "/input/bar_enable")

    # Das Dashboard ist immer aktiv
    weather_station.add_ui(dashboard_ui)

    # MQTT-Thread starten
    mqtt_client.loop_start()

    # Programmschleife
    try:
        while True:
            # Ca. alle 5 Sekunden neue Sensorwerte einlesen und die Anzeigen aktualisieren
            weather_station.loop()
            time.sleep(5)
    except KeyboardInterrupt:
        # Programm beenden
        pass
    finally:
        weather_station.cleanup()
        mqtt_client.loop_stop()
        mqtt_client.disconnect()