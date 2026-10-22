"""
Python Weather App

A simple terminal app that shows the current weather for a city
using the OpenWeatherMap Current Weather API.

Usage:
    python weather.py
"""

import os
import sys

import requests
from dotenv import load_dotenv

API_URL = "https://api.openweathermap.org/data/2.5/weather"
REQUEST_TIMEOUT_SECONDS = 10
MAX_CITY_NAME_LENGTH = 100
SEPARATOR = "=" * 40


class WeatherError(Exception):
    """An error with a message that is safe to show to the user.

    These messages never include the API key.
    """


def load_api_key():
    """Load WEATHER_API_KEY from the .env file next to this script."""
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    load_dotenv(env_path)

    api_key = os.getenv("WEATHER_API_KEY", "").strip()
    if not api_key:
        raise WeatherError(
            "No API key found.\n"
            "Open (or create) the .env file in the project folder and add your key like this:\n"
            "    WEATHER_API_KEY=your_api_key_here\n"
            "You can get a free key at https://openweathermap.org/api"
        )
    return api_key


def validate_city_name(city):
    """Return an error message if the city name is invalid, otherwise None."""
    if not city:
        return "City name cannot be empty."
    if len(city) > MAX_CITY_NAME_LENGTH:
        return "City name is too long (maximum {} characters).".format(MAX_CITY_NAME_LENGTH)
    if not any(char.isalpha() for char in city):
        return "City name must contain at least one letter."
    return None


def ask_for_city():
    """Keep asking the user for a city name until a valid one is entered."""
    while True:
        city = input("Enter a city name: ").strip()
        error = validate_city_name(city)
        if error is None:
            return city
        print("Error: " + error + " Please try again.\n")


def fetch_weather(city, api_key):
    """Request the current weather for a city and return the JSON data.

    We never include the original exception text in our messages, because
    Requests errors can contain the full URL, which includes the API key.
    """
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
    }

    try:
        response = requests.get(API_URL, params=params, timeout=REQUEST_TIMEOUT_SECONDS)
    except requests.exceptions.Timeout:
        raise WeatherError(
            "The request timed out after {} seconds. Please try again later.".format(
                REQUEST_TIMEOUT_SECONDS
            )
        )
    except requests.exceptions.ConnectionError:
        raise WeatherError(
            "Could not connect to the weather service. "
            "Please check your internet connection."
        )
    except requests.exceptions.RequestException:
        raise WeatherError("Something went wrong while contacting the weather service.")

    # Turn common HTTP error codes into friendly messages.
    status = response.status_code
    if status == 400:
        raise WeatherError("'{}' is not a valid city name.".format(city))
    if status == 401:
        raise WeatherError(
            "The API key is invalid or not yet active.\n"
            "Check the key in your .env file. New keys can take up to "
            "a couple of hours to activate."
        )
    if status == 404:
        raise WeatherError("City '{}' was not found. Check the spelling and try again.".format(city))
    if status == 429:
        raise WeatherError("Too many requests (rate limit exceeded). Please wait and try again.")
    if status != 200:
        raise WeatherError("The weather service returned an error (HTTP {}).".format(status))

    try:
        return response.json()
    except ValueError:
        raise WeatherError("The weather service sent back data that is not valid JSON.")


def parse_weather(data):
    """Pick out the fields we need from the API response.

    Returns a dictionary with simple keys, or raises WeatherError
    if the response does not look the way we expect.
    """
    try:
        return {
            "city": data["name"],
            # Some locations (e.g. remote islands) have no country code.
            "country": (data.get("sys") or {}).get("country") or "N/A",
            "temperature": float(data["main"]["temp"]),
            "feels_like": float(data["main"]["feels_like"]),
            "condition": data["weather"][0]["main"],
            "description": data["weather"][0]["description"].capitalize(),
            "humidity": int(data["main"]["humidity"]),
            "wind_speed": float(data["wind"]["speed"]),
        }
    except (KeyError, IndexError, TypeError, ValueError, AttributeError):
        raise WeatherError("The weather data was missing expected information.")


def display_weather(weather):
    """Print the weather information in a neat format."""
    print()
    print(SEPARATOR)
    print("  Current Weather: {}, {}".format(weather["city"], weather["country"]))
    print(SEPARATOR)
    print("  Temperature : {:.1f} °C".format(weather["temperature"]))
    print("  Feels like  : {:.1f} °C".format(weather["feels_like"]))
    print("  Condition   : {}".format(weather["condition"]))
    print("  Description : {}".format(weather["description"]))
    print("  Humidity    : {}%".format(weather["humidity"]))
    print("  Wind speed  : {:.1f} m/s".format(weather["wind_speed"]))
    print(SEPARATOR)
    print()


def main():
    """Run the weather app. Returns 0 on success and 1 on error."""
    print(SEPARATOR)
    print("  Python Weather App")
    print(SEPARATOR)

    try:
        api_key = load_api_key()
        city = ask_for_city()
        data = fetch_weather(city, api_key)
        weather = parse_weather(data)
    except WeatherError as error:
        print("\nError: {}".format(error))
        return 1
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")
        return 1

    display_weather(weather)
    return 0


if __name__ == "__main__":
    sys.exit(main())
