# SPDX-FileCopyrightText: 2022 Sameer Charles for Magical Apes
# SPDX-License-Identifier: MIT
#
"""
lib_cp_magicalapes/output/display_ssd1306
====================================================

OLED SSD1306 utility - adafruit_ssd1306 extension

"""

import busio
import adafruit_ssd1306


class _OLED():
    
    def circ(self,x,y,r, *, fill=1,color=1):
        for i in range(x-r,x+r+1):
            for j in range(y-r,y+r+1):
                if fill==1:
                    if((i-x)**2 + (j-y)**2 < r**2):
                        self.pixel(i,j,1)
                else:
                    if((i-x)**2 + (j-y)**2 < r**2) and ((i-x)**2 + (j-y)**2 >= (r-r*fill-1)**2):
                        self.pixel(i,j,color)

    def _draw_image_ascii(self, file, color, shift_x: int = 0, shift_y: int = 0):
        lines = file.readlines()
        for ln, line in enumerate(lines):
            line_text = line.strip().decode('utf-8')
            for cn, c in enumerate(line_text):
                # if char is not 0 we set the pixel, that will take care
                # of any other chars mistakenly/for-fun added to the image, eg ASCII art
                x = cn  + shift_x
                y = ln + shift_y
                if c is '0':
                    if x < self.width and y < self.height:
                        self.pixel(x, y, color)

    def _draw_image_p1(self, file, color, shift_x: int = 0, shift_y: int = 0):
        line = file.readline() # line containing dimension, ignore
        while line.startswith(b'#') is True: # lines containing file name or comments
            line = file.readline()
        self._draw_image_ascii(file, color, shift_x, shift_y)

    def _draw_image_p4(self, file, color, shift_x: int = 0, shift_y: int = 0):
        line = file.readline()
        while line.startswith(b'#') is True:
            line = file.readline()
        data = bytearray(file.read())
        for byte in range(self.width // 8 * self.height):
            for bit in range(8):
                if data[byte] & 1 << bit == 0:
                    x = (((8-bit) + (byte * 8)) % self.width) + shift_x
                    y = (byte * 8 // self.width) + shift_y
                    if x < self.width and y < self.height:
                        self.pixel(x, y, color)

    def draw_image(self, filename, color, shift_x: int = 0, shift_y: int = 0):
        with open(filename, 'rb') as f:
            line = f.readline()
            if line.startswith(b'P4') is True:
                self._draw_image_p4(f, color, shift_x, shift_y)
            elif line.startswith(b'P1') is True:
                self._draw_image_p1(f, color, shift_x, shift_y)
            else:
                self._draw_image_ascii(f, color, shift_x, shift_y)

            f.close()

class Display_I2C(adafruit_ssd1306.SSD1306_I2C, _OLED):

    def __init__(self, width: int, height: int, i2c: busio.I2C, *, addr: int = 0x3C):
        self.width = width
        self.height = height
        super(Display_I2C, self).__init__(
            width,
            height,
            i2c,
            addr = addr
            )
