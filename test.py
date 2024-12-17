from tkinter import *
import tkinter as tk
import requests
from PIL import Image, ImageTk
from datetime import datetime, timedelta
import ttkbootstrap as ttk

def get_weather(city):
    API_KEY = "d3f7e0c7bf1cec9eb4743debb734a7d0"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    res = requests.get(url)
    data = res.json()
    if res.status_code != 200:
        print(f"Error: {data.get('message', 'Unable to fetch data')}")
        return None
    if "weather" not in data or "main" not in data or "timezone" not in data:
        print("Error: Malformed response from API")
        return None
    icon_id = data["weather"][0]["icon"]
    temperature = data["main"]["temp"] - 273.15
    description = data["weather"][0]["description"]
    city = data["name"]
    country = data["sys"]["country"]
    timezone_offset = data["timezone"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    icon_url = f"http://openweathermap.org/img/wn/{icon_id}@2x.png"
    return (icon_url, temperature, description, city, country, timezone_offset, humidity, wind_speed)

def update_weather_details(result):
    icon_url, temperature, description, city, country, timezone_offset, humidity, wind_speed = result
    location_label.configure(text=f"{city}, {country}")
    utc_time = datetime.utcnow()
    local_time = utc_time + timedelta(seconds=timezone_offset)
    local_time_str = local_time.strftime("%Y-%m-%d %H:%M:%S")
    time_label.configure(text=f"Local Time: {local_time_str}")
    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image=icon)
    icon_label.image = icon
    temperature_label.configure(text=f"{temperature:.2f}°C")
    description_label.configure(text=f"{description.capitalize()}")
    humidity_label.configure(text=f"Humidity: {humidity}%")
    wind_label.configure(text=f"Wind Speed: {wind_speed} m/s")

def search():
    city = city_entry.get()
    result = get_weather(city)
    if result:
        update_weather_details(result)
    else:
        location_label.configure(text="City not found. Try again.")
        icon_label.configure(image='')
        temperature_label.configure(text="")
        description_label.configure(text="")
        time_label.configure(text="")
        humidity_label.configure(text="")
        wind_label.configure(text="")

# Create App Window
root = ttk.Window(themename="litera")
root.title("Professional Weather App")
root.geometry("700x900")

# Header
header_frame = ttk.Frame(root, padding=10)
header_frame.pack(fill="x")

header_label = ttk.Label(header_frame, text="🌤️ Weather App", font=("Helvetica", 28, "bold"), bootstyle="primary")
header_label.pack()

# Entry and Button
input_frame = ttk.Frame(root, padding=20)
input_frame.pack()

city_entry = ttk.Entry(input_frame, font=("Helvetica", 16), width=25)
city_entry.pack(side="left", padx=10)

search_button = ttk.Button(input_frame, text="Search", command=search, bootstyle="success-outline")
search_button.pack(side="left")

# Weather Details
details_frame = ttk.Frame(root, padding=20)
details_frame.pack()

location_label = ttk.Label(details_frame, font=("Helvetica", 24, "bold"))
location_label.pack(pady=10)

time_label = ttk.Label(details_frame, font=("Helvetica", 16))
time_label.pack(pady=5)

icon_label = tk.Label(details_frame)
icon_label.pack(pady=5)

temperature_label = ttk.Label(details_frame, font=("Helvetica", 20, "bold"))
temperature_label.pack(pady=10)

description_label = ttk.Label(details_frame, font=("Helvetica", 18))
description_label.pack(pady=5)

# Additional Info
extra_info_frame = ttk.Frame(root, padding=10)
extra_info_frame.pack()

humidity_label = ttk.Label(extra_info_frame, font=("Helvetica", 16))
humidity_label.pack(pady=5)

wind_label = ttk.Label(extra_info_frame, font=("Helvetica", 16))
wind_label.pack(pady=5)

# Footer
footer_label = ttk.Label(root, text="Powered by OpenWeather • Stay Informed 🌎", font=("Helvetica", 12, "italic"))
footer_label.pack(side="bottom", pady=20)

root.mainloop()
