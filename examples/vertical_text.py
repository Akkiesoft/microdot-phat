#!/usr/bin/env python

import time

import board
from busio import I2C
from microdotphat import MicroDotpHAT

bus = I2C(board.GP5, board.GP4)
mdp = MicroDotpHAT(bus)


print("""Vertical Text

Scrolls text messages vertically.

Press Ctrl+C to exit.
""")

lines = ['One', 'Two', 'Three', 'Four', 'Five']

for line, text in enumerate(lines):
    mdp.write_string(text, offset_y = line*7, kerning=False)

mdp.show()

while True:
    time.sleep(1)
    for x in range(7):
        mdp.scroll_vertical()
        mdp.show()
        time.sleep(0.02)
