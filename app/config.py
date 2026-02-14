import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    MONGODB_URI = os.getenv('MONGODB_URI')
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
    WEATHER_API_BASE_URL = "https://api.openweathermap.org/data/2.5"
