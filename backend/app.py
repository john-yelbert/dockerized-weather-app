from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

# Initialize app
app = Flask(__name__)
CORS(app)

# Load environment variables
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def fetch_weather_data(params):
    """Helper function to make API requests and handle errors."""
    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        # OpenWeather sometimes returns 'cod' != 200 in JSON, even with 200 HTTP
        if str(data.get("cod")) != "200":
            return {"error": data.get("message", "Unknown error occurred")}, int(data.get("cod", 400))

        return data, 200
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}, 500


def format_weather(data):
    """Extract and format relevant weather info."""
    return {
        "city": data.get("name"),
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "weather_main": data["weather"][0]["main"],        
        "description": data["weather"][0]["description"],    
        "icon": data["weather"][0]["icon"],
    }


@app.route("/")
def home():
    return jsonify({"message": "Weather API is running"})


@app.route("/weather", methods=["GET"])
def weather():
    """API endpoint: Get weather data by city OR coordinates."""
    city = request.args.get("city")
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if city:
        params = {"q": city, "appid": API_KEY, "units": "metric"}
    elif lat and lon:
        params = {"lat": lat, "lon": lon, "appid": API_KEY, "units": "metric"}
    else:
        return jsonify({"error": "Please provide a city or latitude & longitude"}), 400

    data, status_code = fetch_weather_data(params)
    if status_code != 200:
        return jsonify(data), status_code

    return jsonify(format_weather(data)), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
