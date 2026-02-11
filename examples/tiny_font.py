#!/usr/bin/env python

import time

from machine import I2C
from microdotphat import MicroDotpHAT

bus = I2C()
mdp = MicroDotpHAT(bus)


print("""Tiny Font

Displays an IP address in a tiny, tiny number font!

Press Ctrl+C to exit.
""")

x = 0

while True:
    mdp.clear()
    mdp.draw_tiny(0,"192")
    mdp.draw_tiny(1,"178")
    mdp.draw_tiny(2,"0")
    mdp.draw_tiny(3,"68")
    mdp.draw_tiny(4,str(x))

    x += 1
    if x > 199: x = 0
    mdp.show()
    time.sleep(0.1)
