from flask import Blueprint

# Create blueprints here
from .victim_routes import victim_bp
from .missing_person_routes import missing_bp
from .relief_camp_routes import camp_bp
from .inventory_routes import inventory_bp
from .donor_routes import donor_bp
from .donation_routes import donation_bp
from .supply_routes import supply_bp
from .volunteer_routes import volunteer_bp
from .assignment_routes import assignment_bp
# For example:
# auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
# disaster_bp = Blueprint('disaster', __name__, url_prefix='/disasters')
# relief_bp = Blueprint('relief', __name__, url_prefix='/relief')

# Function to register all blueprints
def register_blueprints(app):
    # Register blueprints here
    app.register_blueprint(victim_bp)
    app.register_blueprint(camp_bp)
    app.register_blueprint(inventory_bp, url_prefix='/api')
    app.register_blueprint(donor_bp, url_prefix='/api')
    app.register_blueprint(donation_bp, url_prefix='/api')
    app.register_blueprint(supply_bp, url_prefix='/api')
    app.register_blueprint(volunteer_bp, url_prefix='/api')
    app.register_blueprint(assignment_bp, url_prefix='/api')
    app.register_blueprint(missing_bp, url_prefix='/api')
    # For example:
    # app.register_blueprint(auth_bp)
    # app.register_blueprint(disaster_bp)
    # app.register_blueprint(relief_bp)

# Import routes here after creating blueprint
# For example: 
# from .auth_routes import *
# from .disaster_routes import * 