# pylint: disable=missing-module-docstring

import sys
import urllib.parse
import requests

BASE_URI = "https://www.metaweather.com"


def search_city(query):
    '''Look for a given city and disambiguate between several candidates. Return one city (or None)'''
    endpoint = BASE_URI + "/api/location/search/?query=" + query
    response = requests.get(endpoint).json()
    if len(response) == 1:
        return response[0]
    if len(response) > 1:
        print("Your city is ambiguous. Type one of those ?")
        index = 1
        for element in range(len(response)):

            print(index, response[element]['title'])
            index = index + 1

        final_choice = int(input("Type the number\n>"))

        #for i,x in enumerate(response):
        #    if final_choice == x['title']:
        #        final_index = i
        final_choice -= 1
        return response[final_choice]

    if not response:
        print("City not found")
        return None


def weather_forecast(woeid):
    '''Return a 5-element list of weather forecast for a given woeid'''
    '''https://www.metaweather.com/api/location/44418'''
    endpoint = BASE_URI + "/api/location/" + str(woeid)
    response = requests.get(endpoint).json()
    weather = response['consolidated_weather']
    return weather


def main():
    '''Ask user for a city and display weather forecast'''
    query = input("City?\n> ")
    city = search_city(query)
    if type(city) != dict:
        print("This is not a city")
    if city and type(city) == dict:
        weather = weather_forecast(city['woeid'])
        weather.pop(0)
        print(f"Here is the weather in {city['title']}")
        for elements in range(len(weather)):
            print(
                f"{weather[elements]['applicable_date']}: {weather[elements]['weather_state_name']} {round(weather[elements]['the_temp'],1)}°C"
            )


if __name__ == '__main__':
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print('\nGoodbye!')
        sys.exit(0)
