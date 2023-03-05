# SPDX-FileCopyrightText: 2022 Sameer Charles for Magical Apes
# SPDX-License-Identifier: MIT
#
"""
lib_cp_magicalapes/utils
====================================================

Utils

"""

import supervisor, time

class Timer:

    def __init__(self, millis:bool = False):
        self.elapsed_time = 0
        self.millis = millis
        self.start_time = 0

    # Resets every 12 hours (approx)
    # We are working with ticks so this is approximate
    def _housekeeping(self):
        if self.millis and self.elapsed > 43200000:
            self.reset()
        elif self.elapsed > 43200:
            self.reset()

    def measure(self):
        if self.millis:
            # supervisor.ticks_ms() does not seem to be very reliable
            now_time = supervisor.ticks_ms()
            if not self.start_time:
                self.start_time = now_time
        else:
            now_time = time.time()
            if not self.start_time:
                self.start_time = now_time
            
        self.elapsed_time = now_time - self.start_time        
        self._housekeeping()

    def reset(self):
        self.elapsed_time = 0
        if self.millis:
            self.start_time = supervisor.ticks_ms()
        else:
            self.start_time = time.time()

    @property
    def elapsed(self):
        return self.elapsed_time