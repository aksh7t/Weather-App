import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import io

# --- Weather Function ---
def get_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name!")
        return

    api_key = "1f54c768997d1504bd258b1eb5dcfd55"  
    base_url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            city_label.config(text=f"📍 {data['name']}, {data['sys']['country']}")
            temp_label.config(text=f"🌡 Temperature: {data['main']['temp']}°C (Feels like {data['main']['feels_like']}°C)")
            humidity_label.config(text=f"💧 Humidity: {data['main']['humidity']}%")
            wind_label.config(text=f"💨 Wind Speed: {data['wind']['speed']} m/s")
            condition_text = data['weather'][0]['description'].capitalize()
            condition_label.config(text=f"💭 Condition: {condition_text}")

            # --- Icon Handling ---
            icon_code = data['weather'][0]['icon']
            icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"

            icon_response = requests.get(icon_url)
            icon_data = icon_response.content
            icon_image = Image.open(io.BytesIO(icon_data))
            icon_photo = ImageTk.PhotoImage(icon_image)

            weather_icon_label.config(image=icon_photo)
            weather_icon_label.image = icon_photo  # keep reference
        else:
            messagebox.showerror("Error", f"City not found: {city}")
    except requests.exceptions.RequestException:
        messagebox.showerror("Network Error", "Unable to fetch weather data. Check your internet connection.")


# --- Tkinter GUI Setup ---
root = tk.Tk()
root.title("🌦 Weather App")
root.geometry("400x520")
root.resizable(False, False)
root.config(bg="#b3e5fc")

# --- Title ---
title_label = tk.Label(root, text="🌤 Live Weather App", font=("Arial", 20, "bold"), bg="#b3e5fc", fg="#01579b")
title_label.pack(pady=10)

# --- City Input ---
city_entry = tk.Entry(root, font=("Arial", 14), width=25, justify="center", bg="#e1f5fe", borderwidth=2, relief="groove")
city_entry.pack(pady=10)
city_entry.focus()

# --- Button ---
search_button = tk.Button(root, text="Get Weather 🌈", font=("Arial", 13, "bold"), bg="#0288d1", fg="white",
                          activebackground="#0277bd", activeforeground="white", command=get_weather)
search_button.pack(pady=10)

# --- Weather Icon ---
weather_icon_label = tk.Label(root, bg="#b3e5fc")
weather_icon_label.pack(pady=10)

# --- Weather Info Display ---
city_label = tk.Label(root, text="", font=("Arial", 15, "bold"), bg="#b3e5fc", fg="#01579b")
city_label.pack(pady=5)

temp_label = tk.Label(root, text="", font=("Arial", 12), bg="#b3e5fc", fg="black")
temp_label.pack(pady=2)

humidity_label = tk.Label(root, text="", font=("Arial", 12), bg="#b3e5fc", fg="black")
humidity_label.pack(pady=2)

wind_label = tk.Label(root, text="", font=("Arial", 12), bg="#b3e5fc", fg="black")
wind_label.pack(pady=2)

condition_label = tk.Label(root, text="", font=("Arial", 12), bg="#b3e5fc", fg="black")
condition_label.pack(pady=2)

# --- Footer ---
footer = tk.Label(root, text="Powered by OpenWeatherMap", font=("Arial", 10), bg="#b3e5fc", fg="#424242")
footer.pack(side="bottom", pady=10)

# --- Run App ---
root.mainloop()
