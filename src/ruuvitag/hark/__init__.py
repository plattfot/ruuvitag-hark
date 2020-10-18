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

"""Simple http server, that returns data in json.

Based on the http_server_asyncio_rx.py example in the ruuvitag-sensor repo[0].

[0]: https://github.com/ttu/ruuvitag-sensor/blob/master/examples/http_server_asyncio_rx.py

Executes get data for sensors in the background.
Endpoints:
    http://0.0.0.0:5000/data
    http://0.0.0.0:5000/data/{mac}
"""

import getopt
import os
import sys
import toml

from aiohttp import web
from ruuvitag_sensor.ruuvi_rx import RuuviTagReactive

class ArgparseFaux:
    """Get the same interface as argparse's error."""
    def __init__(self, prog=os.path.basename(sys.argv[0])):
        self.prog=prog

    def error(self, message, errno=2):
        print(f"{self.prog}: {message}\nTry `{self.prog} --help' for more information.")
        sys.exit(errno)

class Arguments:
    def __init__(self):
        self.tags = {}
        self.config = None
        self.port=None

def parse_arguments(argv):
    parser = ArgparseFaux(prog=os.path.basename(argv[0]))
    helpstring=f"""usage: {parser.prog} [OPTIONS]...
Simple http server, that returns ruuvitag data in json.

Options:
  -T, --tag MAC=NAME   Specify a ruuvitag to fetch data from
      --config CONFIG  Read settings from a config file
  -p, --port PORT      Set the port number, default 5000
  -h, --help           Print this message then exits
"""
    args = Arguments()
    try:
        opts, args.shell_args = getopt.gnu_getopt(
            argv[1:],
            "hT:",
            ["help",
             "tag=",
             "config=",
             ])
    except getopt.GetoptError as err:
        parser.error(err)

    for option, argument in opts:
        if option in ("-h", "--help"):
            print(helpstring)
            sys.exit(0)
        elif option in ("-T", "--tag"):
            mac_name = argument.split('=')
            args.tags[mac_name[0].lower()] = mac_name[1]
        elif option == "--config":
            args.config = argument

    return parser, args

def parse_config(config, args, parser):
    try:
        for name, data in config['tags'].items():
            try:
                mac_lower = data['mac'].lower()
                if not mac_lower in args.tags:
                    args.tags[mac_lower] = name
            except KeyError:
                pass
    except KeyError:
        pass

    if not args.port:
        try:
            args.port = config['settings']['port']
        except KeyError:
            pass
    return args

def setup_ruuvi(tags, all_data):

    def handle_new_data(data):
        data[1]['name'] = tags[data[0]]
        all_data[data[0]] = data[1]

    ruuvi_rx = RuuviTagReactive(list(tags.keys()))
    data_stream = ruuvi_rx.get_subject()
    data_stream.subscribe(handle_new_data)

def setup_routes(app, all_data):
    async def get_all_data(request):
        return web.json_response(all_data)

    async def get_data(request):
        mac = request.match_info.get('mac')
        if mac not in all_data:
            return web.json_response(status=404)
        return web.json_response(all_data[mac])

    app.router.add_get('/data', get_all_data)
    app.router.add_get('/data/{mac}', get_data)

def run(argv):
    parser, args = parse_arguments(argv)

    if args.config:
        with open(args.config) as config_file:
            args = parse_config(toml.load(config_file), parser, args)

    all_data = {}
    setup_ruuvi(args.tags, all_data)
    # Setup and start web application
    app = web.Application()
    setup_routes(app, all_data)
    web.run_app(app, host='0.0.0.0', port=args.port if args.port else 5000)

def main():
    run(sys.argv)

