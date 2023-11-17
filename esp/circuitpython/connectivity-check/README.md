# Connectivity check

## Requirements

CircuitPython compatible microcontroller. Must have a display. Tested with [ESP32-S2 TFT](https://www.adafruit.com/product/5300) module from Adafruit.

Check if outbound internet connection are open or close.

Checks done:

* ping Google (8.8.4.4)
* Open socket to test.mosquitto.org:1883 (MQTT)
* Open socket to httpbin.org:80 (HTTP)

Shows summary on TFT.
