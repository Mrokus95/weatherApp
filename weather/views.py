from django.shortcuts import render
import requests
import datetime
from django.utils import timezone
from datetime import timedelta
from .models import WeatherHistory
from dotenv import load_dotenv
import os

load_dotenv()
# Create your views here.

def convert_form_unix(unix_time):

    # Converting Unix time to a date and time object.
    datetime_object = datetime.datetime.fromtimestamp(unix_time)

    # Date formatting
    formatted_time = datetime_object.strftime('%H:%M')     

    return formatted_time

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

def get_data(request):

    if request.method == 'POST':
        API_KEY = os.environ['API_KEY']
        # The provided city name from the form.
        city = request.POST.get('city')

        # The provided country code from the form.
        country_code = request.POST.get('country')

        # The provided unit from the form.
        units = request.POST.get('units')
        
        # Validation
        if not city:
            error_message = "Wpisz miasto i kod kraju by zobaczyć pogodę!"
            return render(request, 'my_data.html', {'error_message': error_message})
        elif len(city) > 20 or has_numbers(city):
            error_message = "Nazwa miasta jest nieprawidłowa. Spróbuj ponownie."
            return render(request, 'my_data.html', {'error_message': error_message})
        elif len(country_code) > 3 or has_numbers(country_code) or not country_code:
            error_message = "Kod kraju jest nieprawidłowy. Spróbuj ponownie."
            return render(request, 'my_data.html', {'error_message': error_message})
        else:
            pass

        # Standardization of the received city name.
        city = city.title()

        # Standardization of the received country code.
        country_code = country_code.upper()

        # Checking if there is already a record in the database for the given city within the last hour.
        last_hour = timezone.now() - timedelta(hours=1)
        existing_data = WeatherHistory.objects.filter(city_name=city, country=country_code, unit=units, question_time__gte=last_hour).first()

        if existing_data:
            # If there is existing data in the database, return it.
            return render(request, 'my_data.html', {'data': existing_data})    


        # Create URL request
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&units={units}&lang=pl&appid={API_KEY}' 

        response = requests.get(url)

        if response.status_code == 200: # Data retrieval was successful
            data = response.json()  # Process the JSON response into a Python object

            formated_data = {
            'city_name' : data['name'],
            'weather' : data['weather'][0]['description'],
            'temp' : round(data['main']['temp'],1),
            'temp_feel' : round(data['main']['feels_like'],1),
            'pressure' : data['main']['pressure'],
            'sunrise' : convert_form_unix(data['sys']['sunrise']),
            'sunset' : convert_form_unix(data['sys']['sunset']),
            'country': country_code,
            'unit' : units}

            # Save date in database
            WeatherHistory.objects.create(**formated_data)

            return render(request, 'my_data.html', {'data': formated_data})   
        elif response.status_code == 404 and response.json()['message'] == 'city not found':
            error_message = "Nie znaleziono miasta"
            return render(request, 'my_data.html', {'error_message': error_message})
        else:
            error_message = "Wystąpił problem z zewnętrznym API"
            return render(request, 'my_data.html', {'error_message': error_message})
    else:   
        return render(request, 'my_data.html')  