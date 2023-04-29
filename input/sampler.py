# SPDX-FileCopyrightText: 2023 Sameer Charles for Magical Apes
# SPDX-License-Identifier: MIT
#
"""
lib_cp_magicalapes/input/sampler
====================================================

Blocking analog and digital sampler

"""

import supervisor, time
import board, analogio, digitalio

class Analog():

    def __init__(self, name: str, pin: board.PIN = board.A0):
        self.name = name
        self.input = analogio.AnalogIn(pin)

    @property
    def get_name(self):
        return self.name

    def _avg(self, samples: int, threshold: int, delay_ms: long, conversion: long):
        sample_array = []
        sleep_for = delay_ms / samples / 1000
        while len(sample_array) < samples:
            # Continue to sample until total delay + number of samples taken
            sample_array.append(self.input.value * conversion)
            time.sleep(sleep_for)
        avg = sum(sample_array) / float(len(sample_array))
        del sample_array
        return avg

    def sample(self, samples: int = 2, threshold: int = 1.5, delay_ms: long = 100, conversion: long = 1):
        avg = self._avg(samples, threshold, delay_ms, conversion)
        return True if avg >= threshold else False


class Digital():

    def __init__(self, name: str, pin: board.PIN = board.GP0):
        self.name = name
        self.input = digitalio.DigitalInOut(pin)
        self.input.direction = digitalio.Direction.INPUT
        self.input.pull = digitalio.Pull.DOWN

    @property
    def get_name(self):
        return self.name

    def sample(self, samples: int = 2, threshold: int = 1, delay_ms: long = 100):
        sample_array = []
        sleep_for = delay_ms / samples / 1000
        while len(sample_array) < samples:
            # Continue to sample until total delay + number of samples taken
            sample_array.append(self.input.value)
            time.sleep(sleep_for)

        trueCount = sum(bool(x) for x in sample_array)
        del sample_array
        return True if trueCount >= threshold else False
