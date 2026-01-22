#!/usr/bin/env python

import math
import time

import board
from busio import I2C
from microdotphat import MicroDotpHAT

bus = I2C(board.GP5, board.GP4)
mdp = MicroDotpHAT(bus)


print("""Fading Text

Uses the brightness control to fade between messages.
""")

speed = 5
strings = ["One", "Two", "Three", "Four"]


string = 0
shown = True

mdp.show()

# Start time. Phase offset by math.pi/2
start = time.monotonic()

while True:
    # Fade the brightness in/out using a sine wave
    b = (math.sin((time.monotonic() - start) * speed) + 1) / 2
    mdp.set_brightness(b)

    # At minimum brightness, swap out the string for the next one
    if b < 0.002 and shown:
        mdp.clear()
        mdp.write_string(strings[string], kerning=False)

        string += 1
        string %= len(strings)

        mdp.show()
        shown = False

    # At maximum brightness, confirm the string has been shown
    if b > 0.998:
        shown = True

    # Sleep a bit to save resources, this wont affect the fading speed
    time.sleep(0.01)
