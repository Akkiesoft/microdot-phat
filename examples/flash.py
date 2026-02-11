#!/usr/bin/env python

import time

from machine import I2C
from microdotphat import MicroDotpHAT

bus = I2C()
mdp = MicroDotpHAT(bus)


print("""Flash

Flashes all the elements.

Press Ctrl+C to exit.
""")

t = 0.5

while True:
    mdp.clear()
    mdp.show()
    time.sleep(t)
    for x in range(mdp.width()):
        for y in range(mdp.height()):
            mdp.set_pixel(x,y,1)
    for x in range(6):
        mdp.set_decimal(x,1)
    mdp.show()
    time.sleep(t)
