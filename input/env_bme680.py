# SPDX-FileCopyrightText: 2022 Sameer Charles for Magical Apes
# SPDX-License-Identifier: MIT
#
"""
lib_cp_magicalapes/input/env_bme680
====================================================

Environmental sensor BME680 extension, adds a simple air quality score 0-100
See: https://github.com/adafruit/Adafruit_CircuitPython_BME680

"""

import busio
import adafruit_bme680

class Env_I2C(adafruit_bme680.Adafruit_BME680_I2C):

    def __init__(self, i2c: busio.I2C, *, address: int = 0x77, debug: bool = False):
        super(Env_I2C, self).__init__(
            i2c,
            address = address,
            debug = debug
            )
        self._set_defaults()

    def _set_defaults(self, gb:int = 72000, hb:int = 40, hw:int = 0.25):
        self._gas_baseline = gb
        self._hum_baseline = hb
        self._hum_weighting = hw
        
    @property
    def gas_baseline(self):
        return self._gas_baseline

    @gas_baseline.setter
    def gas_baseline(self, value):
        self._gas_baseline = value

    @property
    def hum_baseline(self):
        return self._hum_baseline

    @hum_baseline.setter
    def hum_baseline(self, value):
        self._hum_baseline = value

    @property
    def hum_weighting(self):
        return self._hum_weighting

    @hum_weighting.setter
    def hum_weighting(self, value):
        self._hum_weighting = value

    @property
    def air_quality(self):
        gas = self.gas
        hum = self.relative_humidity
        
        gas_offset = self.gas_baseline - gas
        hum_offset = hum - self.hum_baseline
        
        # Calculate hum_score as the distance from the hum_baseline.
        if hum_offset > 0:
            hum_score = (100 - self.hum_baseline - hum_offset)
            hum_score /= (100 - self.hum_baseline)
            hum_score *= (self.hum_weighting * 100)

        else:
            hum_score = (self.hum_baseline + hum_offset)
            hum_score /= self.hum_baseline
            hum_score *= (self.hum_weighting * 100)

        # Calculate gas_score as the distance from the gas_baseline.
        if gas_offset > 0:
            gas_score = (gas / self.gas_baseline)
            gas_score *= (100 - (self.hum_weighting * 100))

        else:
            gas_score = 100 - (self.hum_weighting * 100)

        # Calculate air_quality_score.
        return hum_score + gas_score
            
