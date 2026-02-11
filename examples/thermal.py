#!/usr/bin/env python

import time

import microcontroller
from machine import I2C
from microdotphat import MicroDotpHAT

bus = I2C()
mdp = MicroDotpHAT(bus)


print("""Thermal

Displays the temperature measured from chip, using
microcontroller.cpu.temperature

Press Ctrl+C to exit.
""")

delay = 1

while True:
    mdp.clear()
    temp = microcontroller.cpu.temperature
    mdp.write_string( "%.2f" % temp + "c", kerning=False)
    mdp.show()
    time.sleep(delay)
