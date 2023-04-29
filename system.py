# SPDX-FileCopyrightText: 2023 Sameer Charles for Magical Apes
# SPDX-License-Identifier: MIT
#
"""
lib_cp_magicalapes/system
====================================================

Abstracts commonly used system methods

"""

import microcontroller, board, analogio, busio, supervisor, os, gc

class System:

    APE_VERSION = 'Ape 0.1'

    POWER_USB = 1
    POWER_BATTERY = 2

    GOD_MODE_FILE = '/god_mode.txt'

    # 4.2 volt max when Battery is full, when battery goes below or equal 2.8v we must stop draining
    # Hardware must take care of battery management, this is here as a second layer of protection
    # and to make sure battery lasts for a very long time.
    POWER_FULL = 4.2
    POWER_EMPTY = 2.8

    def __init__(self, *, vsys: board.Pin = board.A3):
        if vsys:
            self.vpin = analogio.AnalogIn(vsys)
        else:
            self.vpin = None
        # check 'remove_for_normal_operation' file
        try:
            with open(self.GOD_MODE_FILE, 'r') as f:
                self._god_mode = True
        except:
            self._god_mode = False

    @property
    def version(self):
        return self.APE_VERSION

    @property
    def machine(self):
        return os.uname().machine

    @property
    def chipset(self):
        return os.uname().sysname

    @property
    def os_release(self):
        return os.uname().release

    @property
    def os_version(self):
        return os.uname().version

    # Power source
    # @return Meta.USB or Meta.BATTERY
    @property
    def power_source(self):
        return self.POWER_USB if supervisor.runtime.usb_connected else self.POWER_BATTERY

    # Helper for quick access
    @property
    def is_charging(self):
        return True if self.power_source == self.POWER_USB else False

    # @return Total voltage available on vsys pin
    @property
    def voltage(self):
        if self.vpin:
            return (self.vpin.value * self.vpin.reference_voltage) / 65536
        else:
            return 0

    @property
    def has_enough_power(self):
        return True if self.voltage > self.POWER_EMPTY else False

    # @return total RAM available in bytes
    @property
    def mem_avail(self):
        return gc.mem_free()

    # @return CPU temperature
    @property
    def temp(self):
        return microcontroller.cpu.temperature

    # Can be called to garbage collect and other housekeeping
    def housekeeping(self):
        gc.collect()

    def open_i2c(self, SCL, SDA, freq=400_000):
        return busio.I2C(SCL, SDA, frequency=freq)

    @property
    def god_mode(self):
        return self._god_mode

    def exists(self, path:str):
        try:
            with open(path, 'r') as f:
                return True
        except:
            return False

    def switch_god_mode(self):
        if self.god_mode:
            # Existing god mode, no switch required
            return True
        try:
            with open(self.GOD_MODE_FILE, 'w') as f:
                f.write("God mode is on! remove this file to switch back to the normal operation")
                self._god_mode = True
                return True
        except:
            return False
