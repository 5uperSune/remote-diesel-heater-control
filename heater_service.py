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
import time

# GPIO pin configuration
PIN_LED_GREEN = 18  # ON indicator
PIN_LED_RED = 19    # OFF indicator

# Minimum seconds between state changes (protects heater hardware)
MIN_TOGGLE_INTERVAL = 10


class HeaterService:
    def __init__(self):
        self._is_on = False
        self._last_toggle = 0

        # Initialize LED pins as outputs
        self._led_green = Pin(PIN_LED_GREEN, Pin.OUT)
        self._led_red = Pin(PIN_LED_RED, Pin.OUT)

        # Set initial state: heater is OFF, so red LED on
        self._led_green.off()
        self._led_red.on()

    def _rate_limit_ok(self):
        """Check if enough time has passed since last toggle."""
        now = time.time()
        if now - self._last_toggle < MIN_TOGGLE_INTERVAL:
            print("Heater: Rate limited (wait {}s)".format(
                MIN_TOGGLE_INTERVAL - (now - self._last_toggle)))
            return False
        self._last_toggle = now
        return True

    def turn_on(self):
        if self._is_on:
            return True
        if not self._rate_limit_ok():
            return False
        self._is_on = True
        self._led_green.on()
        self._led_red.off()
        print("Heater: ON")
        return True

    def turn_off(self):
        if not self._is_on:
            return True
        if not self._rate_limit_ok():
            return False
        self._is_on = False
        self._led_green.off()
        self._led_red.on()
        print("Heater: OFF")
        return True

    def is_on(self):
        return self._is_on

    def status(self):
        return "ON" if self._is_on else "OFF"
