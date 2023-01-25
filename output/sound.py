# SPDX-FileCopyrightText: 2022 Sameer Charles for Magical Apes
# SPDX-License-Identifier: MIT
#
"""
lib_cp_magicalapes/output/sound
====================================================

Supports pwm tone output:
- Blocking -> specified duration
- Continuous -> until stop() is called

"""

import time, board, pwmio

class Tone:

    def __init__(self, pin: board.PIN = board.GP1):
        self.pwm = None
        self.pin = pin
        self.playing = False

    def play(self, freq, duration:int = 0):
        if duration: # blocking
            with pwmio.PWMOut(
                self.pin, frequency=int(freq), variable_frequency=False
            ) as pwm:
                pwm.duty_cycle = 0x8000
                time.sleep(duration)    
        else: # continuous, call stop() to deinit
            self.pwm = pwmio.PWMOut(self.pin, frequency=int(freq), variable_frequency=False)
            self.pwm.duty_cycle = 0x8000
            self.playing = True

    @property
    def is_playing(self):
        return self.playing

    def stop(self):
        if self.pwm:
            self.pwm.deinit()

