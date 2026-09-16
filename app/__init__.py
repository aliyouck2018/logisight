"""Flask application factory for LogiSight."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import logging
import os

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name=None):
    """Create and configure the Flask application.
    
    Args:
        config_name: Configuration mode ('development', 'testing', 'production')
        
    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    from app.config import config
    app.config.from_object(config.get(config_name, config['development']))
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # Create instance folder
    os.makedirs(app.instance_path, exist_ok=True)
    
    # Configure logging
    setup_logging(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app


def setup_logging(app):
    """Configure application logging."""
    if not app.debug:
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        )
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)
        app.logger.setLevel(logging.INFO)
    else:
        app.logger.setLevel(logging.DEBUG)
