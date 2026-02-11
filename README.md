![Micro Dot pHAT](microdot-phat-logo.png)
https://shop.pimoroni.com/products/microdot-phat

Micro Dot pHAT is an unashamedly old school LED matrix display board, with up to 30x7 pixels, using the Lite-On LTP-305 matrices. Perfect for building a retro scrolling message display or a tiny 30 band spectrum analyser.

## This is a forked for CircuitPython.

This branch contains a modified library enabling the Micro Dot pHAT to operate with CircuitPython.

Compared to the original, modifications have been made to avoid using numpy (I employed AI for the code alterations).

While coding for hardware initialisation has become necessary, all other functions remain compatible with the original.

```
import board
from busio import I2C
from microdotphat import MicroDotpHAT

bus = I2C(board.GP5, board.GP4)
mdp = MicroDotpHAT(bus)
```

## Installing

Copy the ```library/microdotphat``` directory to /lib in the CIRCUITPY drive.

## Original library

https://github.com/pimoroni/microdot-phat