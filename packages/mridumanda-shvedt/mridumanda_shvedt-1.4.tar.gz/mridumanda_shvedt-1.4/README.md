# Mridu Manda

Mridu-Manda is a minimal console application that shows weather and is based on the OpenWeatherMap API.

## Features

- Compact display of weather
- Supports automatic location detection using ipInfo
- Supports command line city input
- Two different output formats, one liner and default

## Requirements

- Requires an API key from OpenWeatherMap
- Requires Python 3.8 or later
- Requires `requests` module 2.31 or later

## Installation

### From PyPI

```bash
pip install mridumanda_shvedt
```

## Usage

After installing run

```bash
mrdmnd                  # for default display of weather
mrdmnd -o               # for one line display of weather
mrdmnd -g               # for weather display with ascii art
mrdmnd -c Kolkata       # for weather display with city name 
```

If it is first time, you will be prompted to enter your API key from OpenWeatherMap. After it is done, run the program again and enjoy.

## Contributions

Feel free to contribute to the project by opening an issue.

## Credits

The ASCII art for weather representation in this project was created by [Julynx](https://github.com/Julynx). It was taken from [here](https://github.com/Julynx/wthr).


## License

This is licensed under the GNU General Public License version 3.0

## Changelog

### Version 1.4 - Latest Release

- Changed to argparse to better management of command line arguments
- Added the `-c` flag to support entering the city name as a command line argument
- Miscellaneous changes to optimize performance