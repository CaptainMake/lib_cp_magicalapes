# SPDX-FileCopyrightText: 2022 Sameer Charles for Magical Apes
# SPDX-License-Identifier: MIT
#
"""
lib_cp_magicalapes/output/lights
====================================================

Encapsulates Neopixel and simple LEDs

"""
import time, board, pwmio, digitalio, neopixel, array

CLEAR = (0, 0, 0)

class Pixel:
    
    def __init__(self, pin: board.PIN, *, n_pixels:int = 1, pixel_order=neopixel.RGB, brightness:int=0.1, auto_write:bool=True):
        self.strip = neopixel.NeoPixel(pin, n_pixels, pixel_order=pixel_order, brightness=brightness, auto_write=auto_write)
        self.n_pixels = n_pixels

    @property
    def brightness(self):
         return self.strip.brightness

    @brightness.setter
    def brightness(self, value:int):
         self.strip.brightness = value

    def clear(self):
        for i in range(self.n_pixels):
            self.strip[i] = CLEAR
        self.brightness = 0.1 # reset brightness

    def show(self, color_array):
        for i, color in enumerate(color_array):
            self.strip[i] = color
            

class LED:
    
    def __init__(self, pin: board.PIN):
        self.led = digitalio.DigitalInOut(pin)
        self.led.direction = digitalio.Direction.OUTPUT
        
    def on(self):
        self.led.value = True
        
    def off(self):
        self.led.value = False
        
    def toggle(self):
        self.led.value = not self.led.value
        
    def blink(self, count:int = 2, delay:int = 0.1):
        for i in range(count):
            self.toggle()
            time.sleep(delay)
            
            
class LED_PWM:
    
    def __init__(self, pin: board.PIN, *, brightness:int = 8000):
        self.pwm = pwmio.PWMOut(pin)
        self.state = 0
        self.duty_cycle = brightness

    @property
    def brightness(self):
        return self.duty_cycle

    @brightness.setter
    def brightness(self, value:int):
        if self.duty_cycle != value:
            self.duty_cycle = value
            self.pwm.duty_cycle = self.duty_cycle
        
    def on(self):
        self.pwm.duty_cycle = self.duty_cycle
        self.state = 1
        
    def off(self):
        self.pwm.duty_cycle = 0
        self.state = 0
        
    def toggle(self):
        self.state = 1 - self.state
        self.pwm.duty_cycle = self.duty_cycle * self.state
        
    def blink(self, count:int = 2, delay:int = 0.1):
        for i in range(count):
            self.toggle()
            time.sleep(delay)
            
            