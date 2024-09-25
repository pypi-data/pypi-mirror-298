import os
import requests
from mridumanda_shvedt.weather_ascii import ascii_arts


def get_city_from_ip():
    try:
        ip_info_response = requests.get("https://ipinfo.io/json")
        
        if ip_info_response.status_code!= 200:
            raise Exception("Failed to get location from IP info \nEnter city name manually after the -c flag")
        
        return ip_info_response.json().get('city')
    
    except requests.exceptions.RequestException as e:
        print("Failed to get location from IP info \nEnter city name manually after the -c flag")
        return None


def get_weather(city):
    if city is None:
        city = get_city_from_ip()
    
    API_KEY = get_api_key()
    API_URL = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + API_KEY
    
    try:
        weather_map_response = requests.get(API_URL)
        
        if weather_map_response.status_code is not 200:
            print("Unable to fetch weather data")
            return None
    except requests.exceptions.RequestException as e:
        print("Failed to fetch weather data")
        return None

    weather_data = weather_map_response.json()

    temp = f"{weather_data['main'].get('temp') - 273.15:.2f} °C"
    temp_min = f"{weather_data['main'].get('temp_min') - 273.15:.2f} °C"
    temp_max = f"{weather_data['main'].get('temp_max') - 273.15:.2f} °C"
    hum = f"{weather_data['main'].get('humidity')}%"
    pressure = f"{weather_data['main'].get('pressure')} hPa"
    desc = weather_data['weather'][0].get('description').title()
    id = weather_data['weather'][0].get('id')
    city_name = weather_data['name']
    country = weather_data['sys'].get('country')
    location = f"{city_name}, {country}"

    return [ "", location, temp, "", temp_min, temp_max, hum, "", desc, pressure, " ", id]


def get_api_key():
    api_key_file = os.path.join(os.getenv('HOME'), '.config','mridumanda', 'api_key.txt')

    with open(api_key_file, 'r') as f:
        api_key = f.read().split('=')[1].strip()

    return api_key


def display_weather_data_ascii(weather_data):
    os.system('clear')

    if weather_data[-1] in range(200, 232):
        for i in range(11):
            print(ascii_arts.thunder[i] + f" {weather_data[i]}")
    elif weather_data[-1] in range(300, 321):
        for i in range(11):
            print(ascii_arts.dust[i] + f" {weather_data[i]}")
    elif weather_data[-1] in range(500, 531):
        for i in range(11):
            print(ascii_arts.rain[i] + f" {weather_data[i]}")
    elif weather_data[-1] in range(600, 622):
        for i in range(11):
            print(ascii_arts.snow[i] + f" {weather_data[i]}")
    elif weather_data[-1] in range(701, 781):
        if weather_data[-1] == 701:
            for i in range(11):
                print(ascii_arts.dust[i] + f" {weather_data[i]}")
        elif weather_data[-1] == 711:
            for i in range(11):
                print(ascii_arts.smoke[i] + f" {weather_data[i]}")
        elif weather_data[-1] == 721:
            for i in range(11):
                print(ascii_arts.dust[i] + f" {weather_data[i]}")
        elif weather_data[-1] == 731:
            for i in range(11):
                print(ascii_arts.dust[i] + f" {weather_data[i]}")
        elif weather_data[-1] == 741:
            for i in range(11):
                print(ascii_arts.fog[i] + f" {weather_data[i]}")
        elif weather_data[-1] == 751:
            for i in range(11):
                print(ascii_arts.dust[i] + f" {weather_data[i]}")
        elif weather_data[i] == 761:
            for i in range(11):
                print(ascii_arts.dust[i] + f" {weather_data[i]}")
        elif weather_data[-1] == 762:
            for i in range(11):
                print(ascii_arts.ash[i] + f" {weather_data[i]}")
        elif weather_data[-1] == 771:
            for i in range(11):
                print(ascii_arts.squall[i] + f" {weather_data[i]}")
        elif weather_data[i] == 781:
            for i in range(11):
                print(ascii_arts.tornado[i] + f" {weather_data[i]}")
        else:
            for i in range(11):
                print(ascii_arts.dust[i] + f" {weather_data[i]}")
    elif weather_data[-1] == 800:
        for i in range(11):
                print(ascii_arts.clear_day[i] + f" {weather_data[i]}")
    else:
        for i in range(11):
            print(ascii_arts.clouds[i] + f" {weather_data[i]}")


def display_weather_one_liner(weather_data):
    os.system('clear')

    print(f"Location: {weather_data[1]} | Temp: {weather_data[2]} | Humidity: {weather_data[6]} | Pressure: {weather_data[9]} | {weather_data[8]}")


def display_weather(weather_data):
    os.system('clear')

    print(f"Weather data for {weather_data[1]}")
    print(f" {'-' * (len('Weather data for') + len({weather_data[1]}) - 2)} ")
    print(f"Temperature:          {weather_data[2]}")
    print(f"Humidity:             {weather_data[6]}")
    print(f"Min Temperature:      {weather_data[4]}")
    print(f"Max Temperature:      {weather_data[5]}")
    print(f"Condition:            {weather_data[8]}")
    print(f"Pressure:             {weather_data[9]}")