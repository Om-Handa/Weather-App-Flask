import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from weather_utils import get_weather

def show_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showerror("Error", "Please enter a city name.")
        return
    weather = get_weather(city)
    if "error" in weather:
        messagebox.showerror("Error", weather["error"])
        return
    update_background(weather["weather_bg"])
    update_icon(weather["weather_icon"])
    update_weather_info(weather)

def update_background(bg_path):
    global bg_original
    bg_original = Image.open(bg_path)
    resize_background()

def resize_background(event=None):
    if not bg_original:
        return
    w, h = root.winfo_width(), root.winfo_height()
    resized = bg_original.resize((w, h))
    bg_image_tk = ImageTk.PhotoImage(resized)
    canvas.bg_image_tk = bg_image_tk
    canvas.itemconfig(bg_item, image=bg_image_tk)
    canvas.coords(title_item, w/2, h*0.12)
    canvas.coords(entry_window, w/2, h*0.25)
    canvas.coords(button_window, w/2, h*0.33)
    canvas.coords(icon_item, w/2 - 80, h*0.6)
    canvas.coords(info_item, w/2 + 80, h*0.6)

def update_icon(icon_path):
    global weather_icon_tk
    icon = Image.open(icon_path).resize((150, 150))
    weather_icon_tk = ImageTk.PhotoImage(icon)
    canvas.itemconfig(icon_item, image=weather_icon_tk, state="normal")

def update_weather_info(weather):
    text = f"{weather['city']}, {weather['country']}\nTemp: {weather['temperature']}°C\nCondition: {weather['condition']}\nHumidity: {weather['humidity']}\nWind Speed: {weather['windkph']}{weather['winddir']}"
    canvas.itemconfig(info_item, text=text)

root = tk.Tk()
root.title("🌤 Weather App")
root.geometry("1200x700")
root.minsize(800, 500)
root.resizable(True, True)

canvas = tk.Canvas(root, highlightthickness=0)
canvas.pack(fill="both", expand=True)

bg_original = Image.open("static/default.jpg")
default_bg_resized = bg_original.resize((1200, 700))
bg_image_tk = ImageTk.PhotoImage(default_bg_resized)
bg_item = canvas.create_image(0, 0, image=bg_image_tk, anchor="nw")

title_item = canvas.create_text(600, 80, text="🌤 Simple Weather App",
                                font=("Arial", 36, "bold"), fill="black")

city_entry = tk.Entry(root, font=("Arial", 20), width=25,
                      bg="white", fg="black", relief="flat", justify="center")
entry_window = canvas.create_window(600, 160, window=city_entry)

check_button = tk.Button(root, text="Check Weather", font=("Arial", 14, "bold"),
                         command=show_weather, bg="#4a90e2", fg="white",
                         activebackground="#357ab7", relief="flat", padx=10, pady=5)
button_window = canvas.create_window(600, 220, window=check_button)

icon_item = canvas.create_image(550, 380, anchor="e", state="hidden")
info_item = canvas.create_text(650, 380, text="", font=("Arial", 22),
                               fill="black", justify="left", anchor="w")

root.bind("<Configure>", resize_background)
root.mainloop()