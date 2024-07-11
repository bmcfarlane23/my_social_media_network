import os  # Import the os module for operating system interactions
from flask import Flask  # Import the Flask class from the flask module
from flask_migrate import Migrate  # Import the Migrate class from the flask_migrate module
from .api.profiles import bp_profiles  # Import the profiles blueprint from the api module
from .api.posts import bp_posts  # Import the posts blueprint from the api module
from .api.images import bp_images  # Import the images blueprint from the api module
from .api.comments import bp_comments  # Import the comments blueprint from the api module
from .models import db  # Import the database instance from the models module
from dotenv import load_dotenv  # Import the load_dotenv function from the dotenv module


# https://flask.palletsprojects.com/en/2.0.x/patterns/appfactories/

# Load environment variables from .env file
load_dotenv()

def create_app(test_config=None):  # Define the application factory function
    app = Flask(__name__, instance_relative_config=True)  # Create an instance of the Flask application
    app.config.from_mapping(  # Set default configuration
        SECRET_KEY=os.getenv('SECRET_KEY'),  # Set the secret key for the application (Example: 'key_name')
        SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL'),  # Set the database URI (Example: 'postgresql://postgres@pg:5432/social_media_app_db')
        SQLALCHEMY_TRACK_MODIFICATIONS=False,  # Disable SQLAlchemy event system
        SQLALCHEMY_ECHO=True  # Enable SQLAlchemy logging
    )

    if test_config is None:  # Check if test_config is not provided
        app.config.from_pyfile('config.py', silent=True)  # Load configuration from config.py if it exists
    else:  # If test_config is provided
        app.config.from_mapping(test_config)  # Override the configuration with test_config

    try:
        os.makedirs(app.instance_path)  # Ensure the instance folder exists
    except OSError:
        pass  # Ignore the error if the folder already exists

    db.init_app(app)  # Initialize the database with the Flask app
    migrate = Migrate(app, db)  # Initialize migration support with the Flask app and database

    # Register blueprints for different parts of the application
    app.register_blueprint(bp_profiles)  # Register the profiles blueprint
    app.register_blueprint(bp_posts)  # Register the posts blueprint
    app.register_blueprint(bp_images)  # Register the images blueprint
    app.register_blueprint(bp_comments)  # Register the comments blueprint

    return app  # Return the Flask app instance
