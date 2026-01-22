#!/usr/bin/env python

import math
import time

import board
from busio import I2C
from microdotphat import MicroDotpHAT

bus = I2C(board.GP5, board.GP4)
mdp = MicroDotpHAT(bus)

print("""Sine Wave

Displays a sine wave across your pHAT.

Press Ctrl+C to exit.
""")

while True:
    mdp.clear()
    t = time.monotonic() * 10
    for x in range(45):
        y = int((math.sin(t + (x/2.5)) + 1) * 3.5)
        mdp.set_pixel(x, y, 1)
        
    mdp.show()
    time.sleep(0.01)
