from django.shortcuts import render
import os
from dotenv import load_dotenv
import requests

BASE_URL = 'http://api.weatherapi.com/v1'


def index(request):
    """
     Using Weather Api - https://www.weatherapi.com/
    Sign up for a free account at [weatherapi.com](https://www.weatherapi.com/), log in
     and generate your new API key in the dashboard section.

    :param request:
    :return:
    """

    load_dotenv()  # reads WEATHERAPI_KEY from .env
    api_key = os.environ.get("WEATHERAPI_KEY")

    if request.method == 'POST':
        city = request.POST.get('city').lower()
        print(city)

        if api_key:
            request_url = f"{BASE_URL}/current.json?key={api_key}&q={city}&aqi=no"  # checking city with API

            response = requests.get(request_url)

            if response.status_code == 200:
                data = response.json()
                location = data['location']
                weather = data['current']
                # print(weather)
                print(location['tz_id'])
                print(weather['temp_c'])

                context = {
                    'weather': weather['temp_c'],
                    'city_name': location['name'],
                    'region': location['region'],
                    'country': location['country'],
                    'lat': location['lat'],
                    'lon': location['lon'],
                    'localtime': location['localtime'],
                    'continent': location['tz_id'],
                    'static_city': city
                }

                return render(request, 'index.html', context)

            else:
                print("An error occurred")
                return render(request, 'index.html', {'static_city': city, 'checker': 'Please enter valid city'})

        elif city == '':
            print('No value')
            return render(request, 'index.html', {'checker': 'Please enter valid info...!'})

        else:
            print('Please add your generated API key into the .env file')
            return render(request, 'index.html', {'checker': 'Please add your generated WEATHERAPI_KEY'})

    return render(request, 'index.html', {})
