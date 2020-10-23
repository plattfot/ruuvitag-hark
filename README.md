# Ruuvitag Hark

Simple http server, that returns data in json.

Based on the http_server_asyncio_rx.py example in the
[ruuvitag-sensor repo](https://github.com/ttu/ruuvitag-sensor/blob/master/examples/http_server_asyncio_rx.py).

## Install

Clone this repo then run `pip install <path to clone>`.

## Usage

Simply run `ruuvitag-hark` with a list of MAC addresses for the
ruuvitags that it should listen to.

```
RUUVI_BLE_ADAPTER="Bleson" ruuvitag-hark --tag 00:11:22:33:44:55=kitchen --tag AA:BB:CC:DD:EE:FF=balcony
```

By default it will listen to port `5000`, but can be changed using
`-p/--port N` where `N` is the new port number.

Then to fetch the data simply visit the machine running
`ruuvitag-hark` with a webbrowser or another tool that can speak http.
For example fetch the data with [curl](https://curl.haxx.se/) and
pretty print it with [jq](https://stedolan.github.io/jq/) on the same
machine running `ruuvitag-hark`

```
$ curl localhost:5000/data|jq
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   382  100   382    0     0   373k      0 --:--:-- --:--:-- --:--:--  373k
{
  "00:00:00:00:00:00": {
    "data_format": 5,
    "humidity": 81.2,
    "temperature": 12.04,
    "pressure": 1011.26,
    "acceleration": 0,
    "acceleration_x": 0,
    "acceleration_y": 0,
    "acceleration_z": 0,
    "tx_power": 4,
    "battery": 2989,
    "movement_counter": 135,
    "measurement_sequence_number": 51772,
    "mac": "000000000000",
    "time": "2020-10-17T00:10:22.287835",
    "name": "balcony"
  }
}
```

### Using systemd

Simply copy the `ruuvitag-hark.service` to
`$XDG_CONFIG_HOME/systemd/user` or `$HOME/.config` if the former is
not set.

```
mkdir -p $XDG_CONFIG_HOME/systemd/user
cp ruuvitag-hark.service $XDG_CONFIG_HOME/systemd/user
```

Create a `config.toml` at `$XDG_CONFIG_HOME/ruuvitag-hark/`, you can
use the `examples/example-config.toml` as a template.

```
mkdir -p $XDG_CONFIG_HOME/ruuvitag-hark
cp `examples/example-config.toml` $XDG_CONFIG_HOME/ruuvitag-hark/config.toml
# edit $XDG_CONFIG_HOME/ruuvitag-hark/config.toml
```

To allow your user to run processes without being logged in, run:
```
loginctl enable-linger $USER
```

Reload the systemd daemon to pick up the service:

```
systemctl --user daemon-reload
```

And enable and start the `ruuvitag-hark.service` by running:

```
systemctl --user enable --now ruuvitag-hark.service
```
