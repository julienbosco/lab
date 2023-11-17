import board
import digitalio
import wifi
from adafruit_display_text import label
import terminalio
import ipaddress
import time
import displayio
import adafruit_requests
import socketpool

display = board.DISPLAY

google = label.Label(terminalio.FONT, text="Google: N/A", color=0x00FF00, scale=2)
google.x = 10
google.y = 10

mqtt_label = label.Label(terminalio.FONT, text="MQTT: N/A", color=0x0000FF, scale=2)
mqtt_label.x = 10
mqtt_label.y = 40

http_label = label.Label(terminalio.FONT, text="HTTP: N/A", color=0x0000FF, scale=2)
http_label.x = 10
http_label.y = 70

display_group = displayio.Group()
display_group.append(google)
display_group.append(mqtt_label)
display_group.append(http_label)
display.show(display_group)

pool = socketpool.SocketPool(wifi.radio)

while True:
    ping_resp = wifi.radio.ping(ipaddress.ip_address("8.8.4.4"), timeout=0.08)
    if(ping_resp):
        google.text = "Google: " + str(ping_resp*1000) + " ms"
        google.color=0x00FF00
    else:
        google.text = "Google: N/A"
        google.color = 0xFF0000
    
    mqtt_socket = pool.socket()
    mqtt_socket.settimeout(1)

    http_socket = pool.socket()
    http_socket.settimeout(1)
    mosquito_addr = pool.getaddrinfo("test.mosquitto.org",1883,0,pool.SOCK_STREAM)[0][-1]
    try:
        mqtt_socket.connect((mosquito_addr[0],mosquito_addr[1]))
        mqtt_label.color = 0x00FF00
        mqtt_label.text = "MQTT (1883): OK"
    except OSError as exc:
        mqtt_label.color = 0xff0000
        mqtt_label.text = "MQTT (1883): Fail"
    finally:
        mqtt_socket.close()

    httpbin_addr = pool.getaddrinfo("httpbin.org",80,0,pool.SOCK_STREAM)[0][-1]
    try:
        http_socket.connect((httpbin_addr[0],httpbin_addr[1]))
        http_label.color = 0x00FF00
        http_label.text = "HTTP (80): OK"
    except OSError as exc:
        http_label.color = 0xff0000
        http_label.text = "HTTP (80): Fail"
    finally:
        http_socket.close()
    
    time.sleep(5)
