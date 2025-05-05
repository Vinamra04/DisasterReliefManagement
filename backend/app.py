from flask import Flask, jsonify
from config import Config
from models import db
from routes import register_blueprints
from flask_migrate import Migrate
from backend import app, db

migrate = Migrate(app, db)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    @app.route('/')
    def index():
        return jsonify({'message': 'Welcome to Disaster Relief Management System API'})
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({'error': 'Server error'}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

