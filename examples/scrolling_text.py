#!/usr/bin/env python

import time
             
import board
from busio import I2C
from microdotphat import MicroDotpHAT

bus = I2C(board.GP5, board.GP4)
mdp = MicroDotpHAT(bus)


print("""Scrolling Text

Scrolls a message across the screen.

Press Ctrl+C to exit.
""")

text = "In the old #BILGETANK we'll keep you in the know!      "

mdp.write_string(text, offset_x=0)

while True:
    mdp.scroll()
    mdp.show()
    time.sleep(0.05)
