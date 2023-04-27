# SPDX-FileCopyrightText: 2022 Sameer Charles for Magical Apes
# SPDX-License-Identifier: MIT
#
"""
lib_cp_magicalapes/output/display_ssd1306
====================================================

OLED SSD1306 utility - adafruit_ssd1306 extension

"""

import time, busio, displayio
import adafruit_ssd1306
import terminalio

import adafruit_displayio_ssd1306
import adafruit_imageload
from adafruit_display_text import label, wrap_text_to_lines

def release():
    # Release all displays
    displayio.release_displays()    

class _OLED():

    def __init__(self, width, height, i2c, addr):
        display_bus = displayio.I2CDisplay(i2c, device_address=addr)
        self.displayio_ssd1306 = adafruit_displayio_ssd1306.SSD1306(display_bus, width=width, height=height)
        
    def circ(self, x, y, r, *, fill=1, color=1):
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

    def label(self, text, x:int=10, y:int=10):
        text = "\n".join(wrap_text_to_lines(text, 18))
        text_area = label.Label(terminalio.FONT, text=text)
        text_area.x = x
        text_area.y = y
        self.displayio_ssd1306.show(text_area)        

    def animate(self, sprite, width, height, frames, *, x:int = 0, y:int = 0, invert:bool = False, repeat:int = 1, fps:int = 20):
        group = displayio.Group()
        icon_bit, icon_pal = adafruit_imageload.load(sprite, bitmap=displayio.Bitmap, palette=displayio.Palette)
        if invert:
            temp = icon_pal[0]
            icon_pal[0] = icon_pal[1]
            icon_pal[1] = temp    
        icon_grid = displayio.TileGrid(icon_bit, pixel_shader=icon_pal, width=1, height=1, tile_height=height, tile_width=width, default_tile=0, x=x, y=y)
        group.append(icon_grid)
        self.displayio_ssd1306.show(group)
        delay = 1 / fps
        while repeat > 0:
            repeat -= 1
            timer = 0
            pointer = 0
            while pointer < frames:
              if (timer + delay) < time.monotonic():
                icon_grid[0] = pointer
                pointer += 1
                timer = time.monotonic()


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
        _OLED.__init__(self, width, height, i2c, addr)