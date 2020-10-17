# Copyright (C) 2020  Fredrik Salomonsson

# This file is part of ruuvitag-hark.

# Ruuvitag-hark is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# Ruuvitag-hark is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with ruuvitag-hark. If not, see
# <https://www.gnu.org/licenses/>.
"""Prints out information from all ruuvitags it can discover

Based on the small example in the readme of
https://github.com/ttu/ruuvitag-sensor

"""
from ruuvitag_sensor.ruuvi import RuuviTagSensor

def main():
    def handle_data(found_data):
        print(f'Found ruuvitag with MAC addres: {found_data[0]}\n{found_data[1]}')

    RuuviTagSensor.get_datas(handle_data)
