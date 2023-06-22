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

    # Konwersja czasu Unix na obiekt daty i czasu
    datetime_object = datetime.datetime.fromtimestamp(unix_time)

    # Formatowanie czasu
    formatted_time = datetime_object.strftime('%H:%M')     

    return formatted_time

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

def get_data(request):

    API_KEY = os.environ['API_KEY']
    # Przekazana nazwa miasta z formularza
    city = request.GET.get('city')

    # Przekazany kod kraju z formularza
    country_code = request.GET.get('country')

    # Przekazana metryka z formularza
    units = request.GET.get('units')
    
    # Walidacja danych wsadowych
    if not city:
        error_message = "Wpisz miasto i kod kraju by zobaczyć pogodę!"
        return render(request, 'my_data.html', {'error_message': error_message})
    elif len(city) > 20 or has_numbers(city):
        error_message = "Nazwa miasta jest nieprawidłowa. Spróbuj ponownie."
        return render(request, 'my_data.html', {'error_message': error_message})
    elif len(country_code) > 3 or has_numbers(country_code) or not country_code:
        error_message = "Kod kraju jest nieprawidłowy.Spróbuj ponownie."
        return render(request, 'my_data.html', {'error_message': error_message})
    else:
        pass

    # Standaryzacja otrzymanej nazwy miasta
    city = city.title()

    # Standaryzacja otrzymanego kodu kraju
    country_code = country_code.upper()

    # Sprawdzenie, czy istnieje już wpis w bazie danych dla danego miasta w ciągu ostatniej godziny
    last_hour = timezone.now() - timedelta(hours=1)
    existing_data = WeatherHistory.objects.filter(city_name=city, country=country_code, unit=units, question_time__gte=last_hour).first()

    if existing_data:
        # Jeśli istnieją dane w bazie, zwróć je
        return render(request, 'my_data.html', {'data': existing_data})    


    # Tworzenie zapytania url
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&units={units}&lang=pl&appid={API_KEY}' 

    response = requests.get(url)

    if response.status_code == 200: # sprawdzenie, czy żądanie było udane
        data = response.json()  # przetworzenie odpowiedzi JSON na obiekt Pythona

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

        # Zapisanie danych w bazie danych
        WeatherHistory.objects.create(**formated_data)

        return render(request, 'my_data.html', {'data': formated_data})   
    elif response.status_code == 404 and response.json()['message'] == 'city not found':
        error_message = "Nie znaleziono miasta"
        return render(request, 'my_data.html', {'error_message': error_message})
    else:
        error_message = "Wystąpił problem z zewnętrznym API"
        return render(request, 'my_data.html', {'error_message': error_message})
    