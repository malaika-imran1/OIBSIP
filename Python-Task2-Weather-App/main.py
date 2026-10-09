import requests

API_KEY = "5e78f2673a1b9bde75cbb7d55e71ac8a"

city = input("Enter city name: ")

url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

try:
    response = requests.get(url, timeout=10)
    data = response.json()

    if response.status_code == 200:
        print("\n===== WEATHER REPORT =====")
        print("City:", data["name"])
        print("Temperature:", data["main"]["temp"], "°C")
        print("Feels Like:", data["main"]["feels_like"], "°C")
        print("Weather:", data["weather"][0]["description"])
        print("Humidity:", data["main"]["humidity"], "%")
        print("Wind Speed:", data["wind"]["speed"], "m/s")
    else:
        print("Error:", data.get("message", "Unable to get weather"))

except requests.exceptions.RequestException:
    print("Network error. Please check your internet connection.")