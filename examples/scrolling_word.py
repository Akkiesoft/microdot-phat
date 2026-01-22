#!/usr/bin/env python

import time
import sys

import board
from busio import I2C
from microdotphat import MicroDotpHAT

bus = I2C(board.GP5, board.GP4)
mdp = MicroDotpHAT(bus)


print("""Scrolling Text

Scrolls a single word char by char across the screen.

Press Ctrl+C to exit.
""")

text = "Ninja"

mdp.write_string(text, offset_x=0, kerning=False)
mdp.show()
time.sleep(0.5)

while True:
    mdp.scroll(amount_x=8)
    mdp.show()
    time.sleep(0.5)
