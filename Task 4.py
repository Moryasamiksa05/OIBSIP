#taks 4

import requests
import json

# Replace 'your_api_key' with the API key you obtained from OpenWeatherMap
API_KEY = "your_api_key"

def get_weather_data(location):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}appid={API_KEY}&q={location}"
    response = requests.get(complete_url)
    return response.json()

def display_weather_data(weather_data):
    if weather_data["cod"] != "404":
        main_data = weather_data["main"]
        temperature = main_data["temp"] - 273.15  # Convert from Kelvin to Celsius
        humidity = main_data["humidity"]
        weather_desc = weather_data["weather"][0]["description"]

        print(f"Temperature: {temperature:.1f}°C")
        print(f"Humidity: {humidity}%")
        print(f"Weather description: {weather_desc.capitalize()}")
    else:
        print("Location not found.")

if __name__ == "__main__":
    user_location = input("Enter the city name or ZIP code: ")
    weather_data = get_weather_data(user_location)
    display_weather_data(weather_data)
