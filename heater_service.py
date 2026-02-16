# heater_service.py
"""
Central service layer for heater control.

Manages heater state and will later handle UART communication
with the actual heater controller.

LED indicators:
- Green LED (GPIO18): Lit when heater is ON
- Red LED (GPIO19): Lit when heater is OFF
"""

from machine import Pin

# GPIO pin configuration
PIN_LED_GREEN = 18  # ON indicator
PIN_LED_RED = 19    # OFF indicator


class HeaterService:
    def __init__(self):
        self._is_on = False

        # Initialize LED pins as outputs
        self._led_green = Pin(PIN_LED_GREEN, Pin.OUT)
        self._led_red = Pin(PIN_LED_RED, Pin.OUT)

        # Set initial state: heater is OFF, so red LED on
        self._led_green.off()
        self._led_red.on()

    def turn_on(self):
        self._is_on = True
        self._led_green.on()
        self._led_red.off()
        print("Heater: ON")

    def turn_off(self):
        self._is_on = False
        self._led_green.off()
        self._led_red.on()
        print("Heater: OFF")

    def is_on(self):
        return self._is_on

    def status(self):
        return "ON" if self._is_on else "OFF"
