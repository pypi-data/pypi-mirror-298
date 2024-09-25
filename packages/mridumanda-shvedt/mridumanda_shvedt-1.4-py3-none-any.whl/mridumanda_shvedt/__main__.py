import argparse
import os
import sys
from mridumanda_shvedt.weather import get_weather, display_weather, display_weather_one_liner, display_weather_data_ascii


def main():
    init()
    
    parser = argparse.ArgumentParser(description="Weather display options and city input")
    
    parser.add_argument('-o', '--one-liner', action='store_true', help='Display weather data in one-liner format')
    parser.add_argument('-g', '--graphical', action='store_true', help='Display weather data with ascii representations')
    parser.add_argument('-c', '--city', type=str, help='Specify city to display weather')
    
    args = parser.parse_args()
    
    weather_data = get_weather(city = args.city) if args.city else get_weather(None)
    
    if weather_data is not None:
        if args.one_liner:
            display_weather_one_liner(weather_data)
        elif args.graphical:
            display_weather_data_ascii(weather_data)
        else:
            display_weather(weather_data)
    else:
        sys.exit(1)


def init():
    program_dir = os.path.join(os.getenv('HOME'), '.config', 'mridumanda')
    
    if not os.path.isfile(os.path.join(program_dir, 'api_key.txt')):
        os.makedirs(program_dir, exist_ok=True)
        
        api_key = input('Enter API key: ')
        
        with open(os.path.join(program_dir, 'api_key.txt'), 'w') as f:
            f.write(f"API={api_key}")
        
        print('API key saved successfully.')
        print('Run the program again, to use it.')
        
        sys.exit(0)