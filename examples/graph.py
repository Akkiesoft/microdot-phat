#!/usr/bin/env python

from time import sleep
from random import randint

import board
from busio import I2C
from microdotphat import MicroDotpHAT

bus = I2C(board.GP5, board.GP4)
mdp = MicroDotpHAT(bus)


print("""Graph

Plots random numbers scross the screen in a bar graph.

Press Ctrl+C to exit.
""")

graph = []
filled = True

while True:
    mdp.clear()
    graph += [randint(0,7)]
    while len(graph) > 45:
        graph.pop(0)

    for x, val in enumerate(graph):
        if filled:
            mdp.set_col(x + (45-len(graph)), [
                0,
                0b1000000,
                0b1100000,
                0b1110000,
                0b1111000,
                0b1111100,
                0b1111110,
                0b1111111][val])
        else:
            mdp.set_col(x, 1 << (7-val))

    mdp.show()
    sleep(0.05)
