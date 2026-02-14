from flask import Blueprint, request, jsonify, current_app
import requests
from flask_jwt_extended import jwt_required
from datetime import datetime

weather_bp = Blueprint('weather', __name__)

def get_owm_icon(icon_name):
    """Map Pirate Weather icon names to OpenWeatherMap icon codes."""
    mapping = {
        'clear-day': '01d',
        'clear-night': '01n',
        'rain': '10d',
        'snow': '13d',
        'sleet': '13d',
        'wind': '50d',
        'fog': '50d',
        'cloudy': '03d',
        'partly-cloudy-day': '02d',
        'partly-cloudy-night': '02n',
        'hail': '13d',
        'thunderstorm': '11d',
        'tornado': '50d'
    }
    return mapping.get(icon_name, '01d') # Default to clear day

@weather_bp.route('', methods=['GET'])
@jwt_required()
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({'message': 'City parameter is required'}), 400
    
    api_key = current_app.config['WEATHER_API_KEY']
    
    # 1. Geocoding (using Open-Meteo free API)
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
    try:
        geo_res = requests.get(geo_url)
        geo_data = geo_res.json()
        
        if not geo_data.get('results'):
            return jsonify({'message': 'City not found'}), 404
            
        location = geo_data['results'][0]
        lat = location['latitude']
        lon = location['longitude']
        city_name = location['name']
        country = location.get('country', '')
        
    except Exception as e:
        return jsonify({'message': 'Error finding city location'}), 500

    # 2. Pirate Weather API Call
    weather_url = f"https://api.pirateweather.net/forecast/{api_key}/{lat},{lon}?units=si&exclude=minutely,hourly"
    
    try:
        weather_res = requests.get(weather_url)
        if weather_res.status_code != 200:
            return jsonify({'message': 'Error fetching weather data'}), weather_res.status_code
            
        data = weather_res.json()
        
        # 3. Process Forecast (Daily)
        daily_forecasts = []
        
        # Pirate Weather 'daily' block
        if 'daily' in data and 'data' in data['daily']:
            for item in data['daily']['data'][:5]: # Get next 5 entries
                # Convert timestamp to date string YYYY-MM-DD
                date_txt = datetime.fromtimestamp(item['time']).strftime('%Y-%m-%d')
                
                daily_forecasts.append({
                    "date": date_txt,
                    "temp": round(item.get('temperatureHigh', 0)), # Use high temp for forecast
                    "description": item.get('summary', 'No description'),
                    "icon": get_owm_icon(item.get('icon', ''))
                })

        # 4. Construct Response
        current = data['currently']
        response = {
            "city": {
                "name": city_name,
                "country": country
            },
            "current": {
                "temp": round(current.get('temperature', 0)),
                "feels_like": round(current.get('apparentTemperature', 0)),
                "humidity": round(current.get('humidity', 0) * 100), # PW returns 0.76, OWM returns 76
                "wind_speed": current.get('windSpeed', 0),
                "description": current.get('summary', 'Clear'),
                "icon": get_owm_icon(current.get('icon', ''))
            },
            "forecast": daily_forecasts
        }

        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'message': f'Weather API Error: {str(e)}'}), 500
