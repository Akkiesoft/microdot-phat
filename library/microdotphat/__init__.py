# -*- coding: utf-8 -*-

"""A library for driving the Pimoroni Micro Dot pHAT Raspberry Pi add-on.

This library creates a virtual buffer of unlimited size onto which you
can write text and icons for scrolling around the Micro Dot pHAT display.

Methods are included for rotating and scrolling, plus writing text either
kerned to one pixel spacing, or spaced to place one character per matrix.

"""

import atexit

from .font import font as _font, tinynumbers as _tinynumbers
from .matrix import NanoMatrix

__version__ = '0.1.0'

WIDTH = 45
HEIGHT = 7

class MicroDotpHAT():
    def __init__(self, bus):
        self.bus = bus

        self.buf = [[0] * WIDTH for _ in range(HEIGHT)]
        self.decimal = [0] * 6

        self.scroll_x = 0
        self.scroll_y = 0

        self.clear_on_exit = True
        self.rotate180 = False
        self.mirror = False

        self.n1 = NanoMatrix(bus, address=0x63)
        self.n2 = NanoMatrix(bus, address=0x62)
        self.n3 = NanoMatrix(bus, address=0x61)

        self.mat = [
            (self.n1, 1), (self.n1, 0),
            (self.n2, 1), (self.n2, 0),
            (self.n3, 1), (self.n3, 0)
        ]

        atexit.register(self._exit)


    def width(self):
        return WIDTH


    def height(self):
        return HEIGHT


    def _exit(self):
        if self.clear_on_exit:
            self.clear()
            self.show()


    def clear(self):
        """Clear the buffer"""

        self.decimal = [0] * 6
        self.buf = [[0] * WIDTH for _ in range(HEIGHT)]
        self.scroll_x = 0
        self.scroll_y = 0


    def fill(self, c):
        """Fill the buffer either lit or unlit

        :param c: Colour that should be filled onto the display: 1=lit or 0=unlit

        """

        for y in range(len(self.buf)):
            for x in range(len(self.buf[y])):
                self.buf[y][x] = c


    def is_connected(self):
        """ Check if a microdot pHat is connected by trying to reach it over I2C.
        Returns True if detected, False if not detected.
        """
        return NanoMatrix.is_connected(self.bus, 0x61) and NanoMatrix.is_connected(self.bus, 0x62) and NanoMatrix.is_connected(self.bus, 0x63)


    def set_clear_on_exit(self, value):
        """Set whether the display should be cleared on exit

        Set this to false if you want to display a fixed message after
        your Python script exits.

        :param value: Whether the display should be cleared on exit: True/False

        """

        self.clear_on_exit = True if value else False


    def set_rotate180(self, value):
        """Set whether the display should be rotated 180 degrees

        :param value: Whether the display should be rotated 180 degrees: True/False

        """

        self.rotate180 = True if value else False


    def set_mirror(self, value):
        """Set whether the display should be flipped left to right (mirrored)

        :param value: Whether the display should be flipped left to right: True/False

        """

        self.mirror = True if value else False


    def set_col(self, x, col):
        """Set a whole column of the buffer

        Only useful when not scrolling vertically

        :param x: Specify which column to set
        :param col: An 8-bit integer, the 7 least significant bits correspond to each row

        """

        for y in range(7):
            self.set_pixel(x, y, (col & (1 << y)) > 0)


    def set_pixel(self, x, y, c):
        """Set the state of a single pixel in the buffer

        If the pixel falls outside the current buffer size, it will be grown automatically

        :param x: The x position of the pixel to set
        :param y: The y position of the pixel to set
        :param c: The colour to set: 1=lit or 0=unlit

        """

        c = 1 if c else 0

        try:
            self.buf[y][x] = c
        except IndexError:
            if y >= len(self.buf):
                while len(self.buf) <= y:
                    self.buf.append([0] * WIDTH)
            if x >= len(self.buf[y]):
                for line in self.buf:
                    while len(line) <= x:
                        line.append(0)
            self.buf[y][x] = c


    def write_char(self, char, offset_x=0, offset_y=0):
        """Write a single character to the buffer

        :param char: The ASCII char to write
        :param offset_x: Position the character along x (default 0)
        :param offset_y: Position the character along y (default 0)

        """

        char = self._get_char(char)

        for x in range(5):
            for y in range(7):
                p = (char[x] & (1 << y)) > 0
                self.set_pixel(offset_x + x, offset_y + y, p)


    def _get_char(self, char):
        char_ordinal = None

        try:
            char_ordinal = ord(char)
        except TypeError:
            pass

        if char_ordinal == 65374:
            char_ordinal = 12316

        if char_ordinal is None or char_ordinal not in _font:
            raise ValueError("Unsupported char {}".format(char))

        return _font[char_ordinal]


    def set_decimal(self, index, state):
        """Set the state of a self.decimal point

        :param index: Index of self.decimal from 0 to 5
        :param state: State to set: 1=lit or 0=unlit

        """

        if index in range(6):
            self.decimal[index] = 1 if state else 0


    def write_string(self, string, offset_x=0, offset_y=0, kerning=True):
        """Write a string to the buffer

        :returns: The length, in pixels, of the written string.

        :param string: The text string to write

        :param offset_x: Position the text along x (default 0)
        :param offset_y: Position the text along y (default 0)
        :param kerning: Whether to kern the characters closely together or display one per matrix (default True)

        :Examples:

        Write a string to the buffer, aligning one character per dislay, This is
        ideal for displaying still messages up to 6 characters long::

            microdotphat.write_string("Bilge!", kerning=False)

        Write a string to buffer, with the characters as close together as possible.
        This is ideal for writing text which you intend to scroll::

            microdotphat.write_string("Hello World!")

        """

        str_buf = []

        space = [0x00] * 5
        gap = [0x00] * 3

        if kerning:
            space = [0x00] * 2
            gap = [0x00]

        for char in string:
            if char == ' ':
                str_buf += space
            else:
                char_data = list(self._get_char(char))
                if kerning:
                    # remove 0 from the beginning and end of the list
                    while char_data and char_data[0] == 0:
                        char_data.pop(0)
                    while char_data and char_data[-1] == 0:
                        char_data.pop()
                str_buf += char_data
            str_buf += gap  # Gap between chars

        if not kerning:
            while len(str_buf) < WIDTH + 3:
                str_buf += [0x00]

        for x in range(len(str_buf)):
            for y in range(7):
                p = (str_buf[x] & (1 << y)) > 0
                self.set_pixel(offset_x + x, offset_y + y, p)

        length = len(str_buf)
        del str_buf
        return length


    def scroll(self, amount_x=0, amount_y=0):
        """Scroll the buffer

        Will scroll by 1 pixel horizontall if no arguments are supplied.

        :param amount_x: Amount to scroll along x axis (default 0)
        :param amount_y: Amount to scroll along y axis (default 0)

        :Examples:

        Scroll vertically::

           microdotphat.scroll(amount_y=1)

        Scroll diagonally::

           microdotphat.scroll(amount_x=1,amount_y=1)

        """

        if amount_x == 0 and amount_y == 0:
            amount_x = 1

        self.scroll_x += amount_x
        self.scroll_y += amount_y
        self.scroll_x %= len(self.buf[0]) if self.buf else WIDTH
        self.scroll_y %= len(self.buf)


    def scroll_to(self, position_x=0, position_y=0):
        """Scroll to a specific position

        :param position_x: Desired position along x axis (default 0)
        :param position_y: Desired position along y axis (default 0)

        """

        self.scroll_x = position_x % (len(self.buf[0]) if self.buf else WIDTH)
        self.scroll_y = position_y % len(self.buf)


    def scroll_horizontal(self, amount=1):
        """Scroll horizontally (along x)

        Will scroll one pixel horizontally if no amount is supplied.

        :param amount: Amount to scroll along x axis (default 1)

        """

        self.scroll(amount_x=amount, amount_y=0)


    def scroll_vertical(self, amount=1):
        """Scroll vertically (along y)

        Will scroll one pixel vertically if no amount is supplied.

        :param amount: Amount to scroll along y axis (default 1)

        """

        self.scroll(amount_x=0, amount_y=amount)


    def set_brightness(self, brightness):
        """Set the display brightness

        :param brightness: Brightness to set, from 0.0 to 1.0

        """

        if brightness < 0 or brightness > 1:
            raise ValueError("Brightness should be between 0.0 and 1.0")

        for m_x in range(6):
            self.mat[m_x][0].set_brightness(brightness)


    def _scroll_buffer(self, buffer, scroll_x, scroll_y):
        """Helper function to scroll buffer horizontally and vertically"""
        if scroll_x == 0 and scroll_y == 0:
            return buffer
        
        # Make a copy
        result = [row[:] for row in buffer]
        
        # Horizontal scroll (roll columns) - reversed direction
        if scroll_x != 0:
            for row in result:
                # Rotate the row in reverse direction
                n = scroll_x % len(row) if row else 0
                row[:] = row[n:] + row[:n]
        
        # Vertical scroll (roll rows) - reversed direction
        if scroll_y != 0:
            n = scroll_y % len(result) if result else 0
            result[:] = result[n:] + result[:n]
        
        return result


    def show(self):
        """Output the buffer to the display

        A copy of the buffer will be scrolled and rotated according
        to settings before being drawn to the display.

        """

        # copy buffer
        scrolled_buffer = [row[:] for row in self.buf]
        
        # padding if needed.
        while len(scrolled_buffer) < HEIGHT:
            scrolled_buffer.append([0] * WIDTH)
        for row in scrolled_buffer:
            while len(row) < WIDTH:
                row.append(0)
        
        # scrolling
        scrolled_buffer = self._scroll_buffer(scrolled_buffer, self.scroll_x, self.scroll_y)
        
        # crop to 7x45
        scrolled_buffer = [row[:45] for row in scrolled_buffer[:7]]
        
        if self.rotate180:
            scrolled_buffer = [list(reversed(row)) for row in reversed(scrolled_buffer)]
        
        if self.mirror:
            scrolled_buffer = [list(reversed(row)) for row in scrolled_buffer]

        for m_x in range(6):
            x = (m_x * 8)
            b = [row[x:x + 5] for row in scrolled_buffer]

            self.mat[m_x][0].set_decimal(self.mat[m_x][1], self.decimal[m_x])

            for x in range(5):
                for y in range(7):
                    try:
                        self.mat[m_x][0].set_pixel(self.mat[m_x][1], x, y, b[y][x])
                    except IndexError:
                        pass  # Buffer doesn't span this matrix yet

        for m_x in range(0, 6, 2):
            self.mat[m_x][0].update()


    def draw_tiny(self, display, text):
        """Draw tiny numbers to the buffer

        Useful for drawing things like IP addresses.
        Can sometimes fit up to 3 digits on a single matrix

        :param display: Index from 0 to 5 of display to target, determines buffer offset
        :param text: Number to display

        """

        _buf = []
        try:
            for num in [int(x) for x in text]:
                _buf += _tinynumbers[num]
                _buf += [0]  # Space

        except ValueError:
            raise ValueError("text should contain only numbers: '{text}'".format(text=text))

        for row in range(min(len(_buf), 7)):
            data = _buf[row]

            offset_x = display * 8
            offset_y = 6 - (row % 7)

            for d in range(5):
                self.set_pixel(offset_x + (4 - d), offset_y, (data & (1 << d)) > 0)
