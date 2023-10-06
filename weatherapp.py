import tkinter as tk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap

root = ttkbootstrap.Window(themename="morph")
root = tk.Tk()
root.title("Weather App")
root.geometry("400x400")

# getting weather from OpenWeatherMap API
def get_weather(city):
    API_key = "ff381492e9ce4c685de816650445595a"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    res = requests.get(url)
    
    if res.status_code == 404:
        messagebox.showerror("Error", "Unable to find city")
        
    # parse json
    weather = res.json()
    icon_id = weather['weather'][0]['icon']
    temperature = weather['main']['temp'] - 273.1
    description = weather ['weather'][0]['description']
    city = weather['name']
    country = weather['sys']['country']
    
    #get icon url and return weather info
    # icon_url = f"https://openweathermap.org/img/wn{icon_id}/@2x.png"
    icon_url = f"https://openweathermap.org/img/wn/{icon_id}/10d@2x.png"
    return (icon_url, temperature, description, city, country)

# search function
def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return

    #if city is found, display weather
    icon_url, temperature, description, city, country = result
    location_label.configure(text=f"{city}, {country}")
    
    #get weather icon image and display icon
    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image=icon)
    icon_label.image = icon
    
    # display temp and description
    temperature_label.configure(text=f"Temperature: {temperature:.2f}°C")
    description_label.configure(text=f"{description}")

# enter city name
city_entry = ttkbootstrap.Entry(root, font="Helvetica, 18")
city_entry.pack(pady=10)

# search button
search_button = ttkbootstrap.Button(root, text="Search", command=search, bootstyle="warning")
search_button.pack(pady=10)

# location title display after search
location_label = tk.Label(root, font="Helvetica, 25")
location_label.pack(pady=20)

# weather icon
icon_label = tk.Label(root)
icon_label.pack(pady=30)

# temperature display 
temperature_label = tk.Label(root, font="Helvetica, 20")
temperature_label.pack()

# description of weather
description_label = tk.Label(root, font="Helvetica, 20")
description_label.pack()

root.mainloop()
