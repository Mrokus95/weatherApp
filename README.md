# WeatherApp

Welcome!

This project is a small weather app that provides simple information about the weather in a city chosen by the user. I have created this application to gain experience with Django and RESTful applications. Below, you will find a list of technologies, the installation process, and the requirements, along with a short description of how to use the WeatherApp. Have fun!

## Technologies

Project is created with:
* Python 3.11
* Django: 4.2.2
* requests: 2.31.0
* python-dotenv: 1.0.0
* HTML
* CSS
* OpenWeatherMap API

## Installation process:

1. Clone the repository to your local computer:

    ```
    $ git clone <adres_repozytorium>
    ```

2. Navigate to the project directory:

    ```
    $ cd weatherApp
    ```

3. (Optional) It is recommended to create and activate a Python virtual environment:

    ```
    $ python -m venv venv
    $ python venv/bin/activate
    ```

4. Install the required dependencies:

    ```
    $ pip install -r requirements.txt
    ```

5. Set the environment variables:

    * `API_KEY` -  OpenWeatherMap API key (you can obtain it from the OpenWeatherMap website)
    * `SECRET_KEY` - Django secret key (automatically generated when creating a Django project)

    You can set the environment variables on your operating system or place them in a .env file in the project's root directory.

6. Run the Django development server:

    ```
    $ python manage.py runserver
    ```

    The application will be available at http://localhost:8000/.

## Usage

    Open a web browser and go to http://localhost:8000/.
    Enter the city name, country code, and select a unit (metric or imperial) in the form.
    Click the "Sprawdź pogodę!" button.

## Note

If weather data for the specified city and unit already exists in the database and is not older than 1 hour, it will be displayed from the database.
Otherwise, the application will fetch the latest weather data from the OpenWeatherMap API, save it in the database, and display it.