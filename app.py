from flask import Flask, render_template, request
from weather_utils import get_weather

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    weather_bg = "static/default.jpg"
    weather_icon = "static/sun.png"
    weather_video = "static/default.mp4"

    if request.method == 'POST':
        city = request.form['city']
        weather_data = get_weather(city)
        if "error" not in weather_data:
            weather_bg = weather_data["weather_bg"]
            weather_video = weather_data["weather_video"]
            weather_icon = weather_data["weather_icon"]

    return render_template(
        'index.html',
        weather=weather_data,
        weather_bg=weather_bg,
        weather_video=weather_video,
        weather_icon=weather_icon
    )

if __name__ == '__main__':
    app.run(debug=True)


