import os  # Import the os module to interact with the operating system
from dotenv import load_dotenv  # Import the load_dotenv function from the dotenv package

# Load environment variables from a .env file into the environment
load_dotenv()  

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')  # Retrieve the secret key from environment variables
    SQLALCHEMY_DATABASE_URI = (  # Construct the database URI for SQLAlchemy
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"  # Include the database user and password from environment variables
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"  # Include the database host, port, and name from environment variables
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking for SQLAlchemy to save resources
    