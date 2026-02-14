from flask import Blueprint, request, jsonify, current_app
import requests
from flask_jwt_extended import jwt_required

weather_bp = Blueprint('weather', __name__)

@weather_bp.route('', methods=['GET'])
@jwt_required()
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({'message': 'City parameter is required'}), 400
    
    api_key = current_app.config['WEATHER_API_KEY']
    base_url = current_app.config['WEATHER_API_BASE_URL']

    # Current Weather
    current_url = f"{base_url}/weather?q={city}&appid={api_key}&units=metric"
    current_res = requests.get(current_url)
    
    if current_res.status_code != 200:
        return jsonify({'message': 'City not found or API error'}), current_res.status_code
    
    current_data = current_res.json()

    # 5-Day Forecast
    forecast_url = f"{base_url}/forecast?q={city}&appid={api_key}&units=metric"
    forecast_res = requests.get(forecast_url)
    
    if forecast_res.status_code != 200:
        return jsonify({'message': 'Error fetching forecast'}), forecast_res.status_code
        
    forecast_data = forecast_res.json()

    # Process Forecast
    daily_forecasts = []
    seen_dates = set()
    
    for item in forecast_data['list']:
        date_txt = item['dt_txt'].split(' ')[0]
        
        if date_txt not in seen_dates:
            seen_dates.add(date_txt)
            daily_forecasts.append({
                "date": date_txt,
                "temp": round(item['main']['temp']),
                "description": item['weather'][0]['description'],
                "icon": item['weather'][0]['icon']
            })
            
    # Limit to 5 days
    daily_forecasts = daily_forecasts[:5]

    response = {
        "city": {
            "name": current_data['name'],
            "country": current_data['sys']['country']
        },
        "current": {
            "temp": round(current_data['main']['temp']),
            "feels_like": round(current_data['main']['feels_like']),
            "humidity": current_data['main']['humidity'],
            "wind_speed": current_data['wind']['speed'],
            "description": current_data['weather'][0]['description'],
            "icon": current_data['weather'][0]['icon']
        },
        "forecast": daily_forecasts
    }

    return jsonify(response), 200
