import requests
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("API_KEY") or "cb42b6b312dd441cb70170954250910"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or "AIzaSyAzQyKUH3UECoFb7Dcl_TOgHNZAxEBg2Mo"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

def get_weather(city: str):
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no"
    response = requests.get(url)
    data = response.json()

    if "error" in data:
        return {"error": data["error"]["message"]}

    condition = data["current"]["condition"]["text"].lower()

    if "sun" in condition or "clear" in condition:
        vbg = "static/sunny.mp4"
        bg = "static/sunny.jpg"
        icon = "static/sun.png"
    elif "rain" in condition or "drizzle" in condition or "shower" in condition:
        vbg = "static/rain.mp4"
        bg = "static/rainy.jpg"
        icon = "static/drizzle.png"
    elif "cloud" in condition or "overcast" in condition:
        vbg = "static/cloudy.mp4"
        bg = "static/cloudy.jpg"
        icon = "static/clouds.png"
    elif "snow" in condition:
        vbg = "static/snow.mp4"
        bg = "static/snow.jpg"
        icon = "static/snowflake.png"
    elif "storm" in condition or "thunder" in condition:
        vbg = "static/thunderstorm.mp4"
        bg = "static/storm.jpg"
        icon = "static/storm.png"
    elif "foggy" in condition or "mist" in condition:
        vbg = "static/foggy.mp4"
        bg = "static/mist.jpg"
        icon = "static/mist.png"
    else:
        vbg = "static/default.mp4"
        bg = "static/default.jpg"
        icon = "static/sun.png"

    weather_info = {
        "city": data["location"]["name"],
        "region": data["location"]["region"],
        "country": data["location"]["country"],
        "temperature": data["current"]["temp_c"],
        "condition": data["current"]["condition"]["text"],
        "windkph": data["current"]["wind_kph"],
        "winddir": data["current"]["wind_dir"],
        "humidity": data["current"]["humidity"],
        "uv": data["current"]["uv"],
        "weather_bg": bg,
        "weather_icon": icon,
        "weather_video": vbg,
    }

    try:
        prompt = (
            f"Write a short friendly 1-2 sentence weather summary for a user.\n"
            f"City: {weather_info['city']}, Country: {weather_info['country']}\n"
            f"Condition: {weather_info['condition']}, Temperature: {weather_info['temperature']}°C, "
            f"Humidity: {weather_info['humidity']}%, Wind: {weather_info['windkph']} kph {weather_info['winddir']}.\n"
            f"Make in hinglish shayri type. dont make it too serious make it funny but in rhyme. no need to tell temperature etc just do it something like mausam achhha hai etc. also give some activities to do in the weather in bullets only 2-3 points"
        )

        response = model.generate_content(prompt)
        summary = response.text.strip()
        weather_info["summary"] = summary

    except Exception as e:
        weather_info["summary"] = "Could not generate Gemini summary."

    return weather_info
