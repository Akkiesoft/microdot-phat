#!/usr/bin/env python

import utime
import ntptime
import network

from machine import I2C
from microdotphat import MicroDotpHAT

bus = I2C()
mdp = MicroDotpHAT(bus)

ssid = "my_wifi"
passphrase = "wifi_password"
TZ_OFFSET = 9

print("""Clock

Displays the time in hours, minutes and seconds

Press Ctrl+C to exit.
""")


sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.active(True)
    sta_if.connect(ssid, passphrase)
    while not sta_if.isconnected():
        print(".")
        utime.sleep(1)
        pass

ntptime.settime()
sta_if.disconnect()
sta_if.active(False)

while True:
    mdp.clear()
    t = utime.localtime(utime.time() + TZ_OFFSET * 3600)
    if t[5] % 2 == 0:
        mdp.set_decimal(2, 1)
        mdp.set_decimal(4, 1)
    else:
        mdp.set_decimal(2, 0)
        mdp.set_decimal(4, 0)
    time_string = "{:02}{:02}{:02}".format(t[3], t[4], t[5])
    mdp.write_string(time_string, kerning=False)
    mdp.show()
    utime.sleep(0.05)
