# from AI
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.http import HttpResponse
import json
import urllib.request
import urllib.parse
import urllib.error


# Create your views here.


def index(request):
    city = ''
    data = {}
    error = ''

    if request.method == 'POST':
        city = request.POST.get('city', '').strip()

        # request.POST is the data sent when the form is submitted with method="post".
        # .get('city', '') looks for the form field named city.
        # If city is missing, it returns an empty string instead of throwing an error.
        # .strip() removes leading and trailing spaces.

        if not city:
            error = 'Please enter a city name.'
        else:
            encoded_city = urllib.parse.quote_plus(city)

            # city is the raw text from the form, like New York
            # urllib.parse.quote_plus(...) converts it into URL-safe text
            # spaces become +
            # special characters are escaped

            url = 'https://api.openweathermap.org/data/2.5/weather?q=' + encoded_city + '&appid=1faa32eae019815ce152f47da804cdd7'

            try:
                res = urllib.request.urlopen(url, timeout=10).read()

                # The timeout is there so the request does not wait forever if the weather API is slow or unreachable.
                # wait at most 10 seconds for the API response if nothing comes back in that time, raise a timeout error your except block then shows a friendly message instead of hanging the page

                json_data = json.loads(res)

                if str(json_data.get('cod')) != '200':
                    error = str(json_data.get('message', 'Unable to fetch weather for this city.'))

                # That block checks whether the weather API returned a successful response or an error response. json_data.get('cod') reads the API status code from the returned JSON. The API uses 200 to mean success. If the code is not 200, it means the API did not return weather data normally. Then error is set to the API’s message, or a default message if message is missing.

                # Why str(...) is used: Sometimes the API returns cod as a number like 200.Sometimes it returns it as a string like "404".Converting to string makes the comparison consistent.

                # 200 is the standard HTTP status for success, but not every API uses the exact same response shape.
                # HTTP uses 2xx codes for success.
                # 200 usually means “OK”.
                # Some APIs return 201 for created, 204 for no content, and other 2xx codes for successful outcomes.



                else:
                    data = {
                        "country_code": str(json_data['sys']['country']),
                        "coordinate": str(json_data['coord']['lon']) + ' ' + str(json_data['coord']['lat']),
                        "temp": str(json_data['main']['temp']) + 'k',
                        "pressure": str(json_data['main']['pressure']),
                        "humidity": str(json_data['main']['humidity']),
                    }
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError):
                error = 'Cannot reach weather service right now. Check internet and try again.'


            # URLError: the request could not be made, often because of DNS, internet, or connection issues
            # HTTPError: the server responded with an HTTP error like 404 or 500
            # TimeoutError: the request took too long



            except (KeyError, ValueError, json.JSONDecodeError):
                error = 'Unexpected weather service response. Please try another city.'


                # KeyError: a dictionary key is missing
                # example: json_data['sys'] does not exist
                # ValueError: the data has the wrong value/format for what you expect
                # json.JSONDecodeError: the response is not valid JSON

                # Why this is needed:
                # Sometimes the API returns an error object instead of weather data
                # Sometimes the response is malformed or incomplete
                # If you try to read fields like sys, coord, or main and they are missing, this block catches the problem

    return render(request, 'index.html', {'data': data, 'city': city, 'error': error})











# from tutorial


# from django.shortcuts import render
# import json
# import urllib.request

# # Create your views here.
# def index(request):
#     if request.method == 'POST':
#         city = request.POST['city']
#         res = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q='+city+'&appid=cb771e45ac79a4e8e2205c0ce66ff633').read()
#         json_data = json.loads(res)
#         data = {
#             "country_code": str(json_data['sys']['country']),
#             "coordinate": str(json_data['coord']['lon']) + ' ' +
#             str(json_data['coord']['lat']),
#             "temp": str(json_data['main']['temp'])+'k',
#             "pressure": str(json_data['main']['pressure']),
#             "humidity": str(json_data['main']['humidity']),
#         }

#     else:
#         city = ''
#         data = {}
#     return render(request, 'index.html', {'city': city, 'data': data})