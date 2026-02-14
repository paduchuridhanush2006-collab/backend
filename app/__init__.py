from flask import Flask
from flask_cors import CORS
from .config import Config
from .extensions import mongo, jwt

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    mongo.init_app(app)
    jwt.init_app(app)
    
    # Configure CORS
    CORS(app)

    # Register blueprints
    from .routes.auth_routes import auth_bp
    from .routes.weather_routes import weather_bp
    from .routes.favorite_routes import favorites_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(weather_bp, url_prefix='/api/weather')
    app.register_blueprint(favorites_bp, url_prefix='/api/favorites')
    
    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}, 200

    return app
