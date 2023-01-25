# SPDX-FileCopyrightText: 2022 Sameer Charles for Magical Apes
# SPDX-License-Identifier: MIT
#
"""
lib_cp_magicalapes/input/motion_lis3dh
====================================================

Sensors lis3dh utility - adafruit_lis3dh extension

"""

import busio
import adafruit_lis3dh

class _Motion():

    force = {
        '2g': adafruit_lis3dh.RANGE_2_G,
        '4g': adafruit_lis3dh.RANGE_4_G,
        '8g': adafruit_lis3dh.RANGE_8_G,
        '16g': adafruit_lis3dh.RANGE_16_G,
    }

    #  - 2G = 40-80 threshold
    #  - 4G = 20-40 threshold
    #  - 8G = 10-20 threshold
    #  - 16G = 5-10 threshold
    def set_defaults(self, force: str = '2g', threshold: int = 60, tap: int = 2):
        self.range = self.force.get(force)
        self.set_tap(tap, threshold)


class Motion_I2C(adafruit_lis3dh.LIS3DH_I2C, _Motion):

    def __init__(self, i2c: busio.I2C, *, address: int = 0x18, int1=None, int2=None):
        super(Motion_I2C, self).__init__(
            i2c,
            address = address
            )

