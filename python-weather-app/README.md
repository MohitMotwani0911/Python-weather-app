# Python Weather App

A simple, beginner-friendly terminal application that shows the current weather for any city using the [OpenWeatherMap](https://openweathermap.org/) Current Weather API.

## Features

- Prompts for a city name and rejects empty or invalid input
- Fetches live current weather from OpenWeatherMap (metric units)
- Displays:
  - City name and country code (shown as `N/A` if the API doesn't provide one)
  - Current temperature (°C)
  - Feels-like temperature (°C)
  - Weather condition and description
  - Humidity (%)
  - Wind speed (m/s)
- Clear, friendly error messages for a missing or invalid API key, unknown cities, rate limits, network problems, timeouts, and unexpected responses
- Keeps your API key out of source code and error messages

## Technology Stack

- Python 3
- [Requests](https://requests.readthedocs.io/) – HTTP requests
- [python-dotenv](https://pypi.org/project/python-dotenv/) – loads settings from a `.env` file
- OpenWeatherMap Current Weather API (`https://api.openweathermap.org/data/2.5/weather`)

## Project Structure

```
python-weather-app/
├── README.md          # This documentation
├── requirements.txt   # Python dependencies
├── weather.py         # The application
├── .env               # Your API key (never commit this file)
└── .gitignore         # Files Git should ignore
```

## Prerequisites

- Python 3.9 or newer. Check your version with:

  ```bash
  python3 --version
  ```

- An internet connection
- A free OpenWeatherMap account

## Setup

### 1. Create and activate a virtual environment (macOS)

From inside the `python-weather-app` folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Your terminal prompt should now start with `(.venv)`. To leave the virtual environment later, run `deactivate`.

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Get an OpenWeatherMap API key

1. Sign up for a free account at [openweathermap.org](https://home.openweathermap.org/users/sign_up).
2. Confirm your email address.
3. Go to the **API keys** tab in your account: <https://home.openweathermap.org/api_keys>.
4. Copy your default key, or generate a new one.

> **Note:** New API keys can take from a few minutes up to a couple of hours to become active. Until then you may see an "invalid API key" error.

### 4. Configure the `.env` file

The `.env` file is not stored on GitHub (it is listed in `.gitignore`), so if you cloned this project you need to create it yourself. In the `python-weather-app` folder, create a file named exactly `.env`. If one already exists, open it in a text editor instead.

Add this line, pasting your key directly after the `=` sign with no spaces or quotes, then save the file:

```
WEATHER_API_KEY=your_api_key_here
```

## Usage

With the virtual environment activated, run:

```bash
python weather.py
```

Type a city name and press **Enter**. You can make the search more specific by adding a country code, for example `London,GB` or `Paris,FR`.

Press **Ctrl+C** at any time to quit.

## Example Output

> The output below is **illustrative only**. Real values will depend on the current weather.

```
========================================
  Python Weather App
========================================
Enter a city name: London

========================================
  Current Weather: London, GB
========================================
  Temperature : 14.3 °C
  Feels like  : 13.6 °C
  Condition   : Clouds
  Description : Broken clouds
  Humidity    : 72%
  Wind speed  : 4.1 m/s
========================================
```

Example of an error (also illustrative):

```
Enter a city name: Atlantisville

Error: City 'Atlantisville' was not found. Check the spelling and try again.
```

## Troubleshooting

| Message | Cause | Fix |
|---|---|---|
| `No API key found.` | `.env` is missing or `WEATHER_API_KEY` is empty | Add your key to `.env` as shown above |
| `The API key is invalid or not yet active.` | HTTP 401: the key is wrong or still activating | Re-copy the key from your OpenWeatherMap account, or wait for it to activate |
| `City '...' was not found.` | HTTP 404: OpenWeatherMap doesn't recognise the city | Check spelling or add a country code, e.g. `Springfield,US` |
| `'...' is not a valid city name.` | HTTP 400: the API rejected the input | Enter a real city name |
| `City name cannot be empty.` | You pressed Enter without typing a city | Type a city name |
| `Too many requests (rate limit exceeded).` | HTTP 429: free-plan call limit reached | Wait a little while and try again |
| `Could not connect to the weather service.` | No internet, DNS, or firewall problem | Check your connection and try again |
| `The request timed out...` | The service took longer than 10 seconds | Try again later |
| `...not valid JSON.` / `...missing expected information.` | Unexpected response from the service | Try again later |
| `ModuleNotFoundError: No module named 'requests'` | Dependencies are not installed, or the virtual environment isn't active | Run `source .venv/bin/activate`, then `python -m pip install -r requirements.txt` |
| `NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+...` | macOS's built-in Python is compiled with LibreSSL | Harmless; the app still works. To remove it, install Python from [python.org](https://www.python.org/downloads/) or Homebrew and recreate the virtual environment |
| `command not found: python` | Virtual environment isn't active | Run `source .venv/bin/activate`, or use `python3` |

## Future Improvements

- Five-day weather forecast
- Choice of units (metric / imperial)
- Weather icons or emoji
- A graphical (GUI) or web interface
- Search history
- Automated tests

## ⚠️ Security Warning

Your `.env` file contains your private API key. **Never commit `.env` to GitHub** or share it publicly. It is already listed in `.gitignore`, so Git will ignore it as long as you don't force-add it. If you ever accidentally publish your key, delete it in your OpenWeatherMap account and create a new one.
