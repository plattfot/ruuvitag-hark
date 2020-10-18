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

import pytest

import ruuvitag.hark
import toml

def test_parse_arguments_tag_long():
    _, args = ruuvitag.hark.parse_arguments(['test', '--tag', '00:00:00:00:00:00=kitchen'])

    assert args.tags['00:00:00:00:00:00'] == 'kitchen'

    _, args = ruuvitag.hark.parse_arguments(['test', '--tag=00:00:00:00:00:00=kitchen'])

    assert args.tags['00:00:00:00:00:00'] == 'kitchen'

def test_parse_arguments_tag_long_multiple():
    _, args = ruuvitag.hark.parse_arguments([
        'test',
        '--tag', '00:00:00:00:00:00=kitchen',
        '--tag', 'AA:BB:CC:DD:EE:FF=bathroom',
    ])

    assert args.tags['00:00:00:00:00:00'] == 'kitchen'
    assert args.tags['aa:bb:cc:dd:ee:ff'] == 'bathroom'

    _, args = ruuvitag.hark.parse_arguments([
        'test',
        '--tag=00:00:00:00:00:00=kitchen',
        '--tag=AA:BB:CC:DD:EE:FF=bathroom',
    ])

    assert args.tags['00:00:00:00:00:00'] == 'kitchen'
    assert args.tags['aa:bb:cc:dd:ee:ff'] == 'bathroom'

def test_parse_arguments_tag_short():
    _, args = ruuvitag.hark.parse_arguments(['test', '-T00:00:00:00:00:00=kitchen'])

    assert args.tags['00:00:00:00:00:00'] == 'kitchen'

    _, args = ruuvitag.hark.parse_arguments(['test', '-T', '00:00:00:00:00:00=kitchen'])

    assert args.tags['00:00:00:00:00:00'] == 'kitchen'

def test_parse_arguments_port_long():

    _, args = ruuvitag.hark.parse_arguments(['test', '--port', '6000'])
    assert args.port == 6000

    _, args = ruuvitag.hark.parse_arguments(['test', '--port=6000'])
    assert args.port == 6000

def test_parse_arguments_port_short():

    _, args = ruuvitag.hark.parse_arguments(['test', '-p', '6000'])
    assert args.port == 6000

    _, args = ruuvitag.hark.parse_arguments(['test', '-p6000'])
    assert args.port == 6000


def test_parse_arguments_tag_long_multiple():
    _, args = ruuvitag.hark.parse_arguments([
        'test',
        '-T', '00:00:00:00:00:00=kitchen',
        '-T', 'AA:BB:CC:DD:EE:FF=bathroom',
    ])

    assert args.tags['00:00:00:00:00:00'] == 'kitchen'
    assert args.tags['aa:bb:cc:dd:ee:ff'] == 'bathroom'

    _, args = ruuvitag.hark.parse_arguments([
        'test',
        '-T00:00:00:00:00:00=kitchen',
        '-Taa:bb:cc:dd:ee:ff=bathroom',
    ])

    assert args.tags['00:00:00:00:00:00'] == 'kitchen'
    assert args.tags['aa:bb:cc:dd:ee:ff'] == 'bathroom'

def test_parse_arguments_name_dupes():
    _, args = ruuvitag.hark.parse_arguments([
        'test',
        '--tag', '00:00:00:00:00:00=kitchen',
        '-TAA:BB:CC:DD:EE:FF=kitchen',
    ])

    assert args.tags['00:00:00:00:00:00'] == 'kitchen'
    assert args.tags['aa:bb:cc:dd:ee:ff'] == 'kitchen'

def test_parse_config():
    parser = ruuvitag.hark.ArgparseFaux(prog='test')
    args = ruuvitag.hark.Arguments()

    config = toml.loads("""
[tags.kitchen]
mac = "00:00:00:00:00:00"

[tags.bathroom]
mac = "AA:BB:CC:DD:EE:FF"

[settings]
port = 6000
""")
    args = ruuvitag.hark.parse_config(config, args, parser)
    assert args.tags['aa:bb:cc:dd:ee:ff'] == 'bathroom'
    assert args.tags['00:00:00:00:00:00'] == 'kitchen'
    assert args.port == 6000

def test_parse_config_mac_dupes():
    parser = ruuvitag.hark.ArgparseFaux(prog='test')
    args = ruuvitag.hark.Arguments()

    config = toml.loads("""
[tags.bathroom1]
mac = "AA:BB:CC:DD:EE:FF"

[tags.bathroom2]
mac = "aa:bb:cc:dd:ee:ff"

""")
    args = ruuvitag.hark.parse_config(config, args, parser)

    assert args.tags['aa:bb:cc:dd:ee:ff'] == 'bathroom1'
    assert not 'AA:BB:CC:DD:EE:FF' in args.tags

def test_parse_config_commandline_override_tag():
    parser, args = ruuvitag.hark.parse_arguments([
        'test',
        '--tag', '00:00:00:00:00:00=balcony',
    ])

    config = toml.loads("""
[tags.kitchen]
mac = "00:00:00:00:00:00"

[tags.bathroom]
mac = "AA:BB:CC:DD:EE:FF"
""")

    args = ruuvitag.hark.parse_config(config, args, parser)
    assert args.tags['aa:bb:cc:dd:ee:ff'] == 'bathroom'
    assert args.tags['00:00:00:00:00:00'] == 'balcony'

def test_parse_config_commandline_override_port():
    parser, args = ruuvitag.hark.parse_arguments([
        'test',
        '-p', '6000'
    ])

    config = toml.loads("""
[settings]
port = 5000
""")

    args = ruuvitag.hark.parse_config(config, args, parser)
    assert args.port == 6000






