# SPDX-FileCopyrightText: 2023 Sameer Charles for Magical Apes
# SPDX-License-Identifier: MIT
#
"""
lib_cp_magicalapes/input/sampler_async
====================================================

Non-blocking analog and digital sampler.

"""

import supervisor, time
import board, analogio, digitalio

class FeedIn():
    def __init__(self, sname: str, dimensions: int = 1, samples: int = 2, threshold: int = 100):
        # Config
        self.sname = sname
        self.dimensions = dimensions
        self.samples = samples
        self.threshold = threshold
        # State
        self.sample_array = [[] for i in range(dimensions)]

    @property
    def name(self):
        return self.sname

    def put(self, *values: long):
        for idx, value in enumerate(values):
            if len(self.sample_array[idx]) >= self.samples:
                self.sample_array[idx] = self.sample_array[idx][1:self.samples]
            self.sample_array[idx].append(value)

    def avg(self):
        res = []
        for dimension in self.sample_array:
            if len(dimension) > 0:
                res.append(sum(dimension) / float(len(dimension)))
            else:
                res.append(0)
        return res

    def result(self):
        avgs = self.avg()
        res = []
        for avg in avgs:
            res.append(True if avg >= self.threshold else False)
        return res

class Analog():

    def __init__(self, sname: str, samples: int = 2, threshold: int = 100, conversion: long = 1, pin: board.PIN = board.A0):
        # Config
        self.sname = sname
        self.samples = samples
        self.threshold = threshold
        self.conversion = conversion
        self.input = analogio.AnalogIn(pin)
        # State
        self.sample_array = []

    @property
    def name(self):
        return self.sname

    @property
    def value(self):
        return self.input.value

    @property
    def sample_count(self):
        return len(self.sample_array)

    def measure(self):
        if len(self.sample_array) >= self.samples:
            self.sample_array = self.sample_array[1:self.samples]
        self.sample_array.append(self.input.value * self.conversion)

    def avg(self):
        return sum(self.sample_array) / float(len(self.sample_array))

    def result(self):
        return True if self.avg() >= self.threshold else False


class Digital():

    def __init__(self, sname: str, samples: int = 2, threshold: int = 100, pin: board.PIN = board.GP0):
        # Config
        self.sname = sname
        self.samples = samples
        self.threshold = threshold
        self.input = digitalio.DigitalInOut(pin)
        self.input.direction = digitalio.Direction.INPUT
        self.input.pull = digitalio.Pull.DOWN
        # State
        self.sample_array = []

    @property
    def name(self):
        return self.sname

    @property
    def value(self):
        return self.input.value

    @property
    def sample_count(self):
        return len(self.sample_array)

    def measure(self):
        if len(self.sample_array) >= self.samples:
            self.sample_array = self.sample_array[1:self.samples]
        self.sample_array.append(self.input.value)

    def result(self):
        trueCount = sum(bool(x) for x in self.sample_array)
        return True if trueCount >= self.threshold else False
