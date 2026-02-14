import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    MONGO_URI = os.getenv('MONGODB_URI') # Flask-PyMongo uses MONGO_URI
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
    WEATHER_API_BASE_URL = "https://api.pirateweather.net"
