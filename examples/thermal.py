#!/usr/bin/env python

import time

import microcontroller
import board
from busio import I2C
from microdotphat import MicroDotpHAT

bus = I2C(board.GP5, board.GP4)
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
