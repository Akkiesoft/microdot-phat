#!/usr/bin/env python

import time
import adafruit_ntp
from rtc import RTC
import adafruit_connection_manager
import wifi

import board
from busio import I2C
from microdotphat import MicroDotpHAT

bus = I2C(board.GP5, board.GP4)
mdp = MicroDotpHAT(bus)

ssid = "my_wifi"
passphrase = "wifi_password"
TZ_OFFSET = 0
ntp_server = "0.pool.ntp.org"

print("""Clock

Displays the time in hours, minutes and seconds

Press Ctrl+C to exit.
""")


wifi.radio.start_station()
wifi.radio.enabled = True
wifi.radio.connect(ssid, passphrase)
pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ntp = adafruit_ntp.NTP(pool, tz_offset=TZ_OFFSET, server=ntp_server)
source = RTC()
source.datetime = ntp.datetime
wifi.radio.enabled = False
wifi.radio.stop_station()


while True:
    mdp.clear()
    t = time.localtime()
    if t.tm_sec % 2 == 0:
        mdp.set_decimal(2, 1)
        mdp.set_decimal(4, 1)
    else:
        mdp.set_decimal(2, 0)
        mdp.set_decimal(4, 0)
    time_string = "{:02}{:02}{:02}".format(t.tm_hour, t.tm_min, t.tm_sec)
    mdp.write_string(time_string, kerning=False)
    mdp.show()
    time.sleep(0.05)
