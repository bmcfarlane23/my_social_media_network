# WSGI stands for Web Server Gateway Interface. It is a specification that describes how a web server communicates 
# with web applications, and how web applications can be chained together to process one request.
from src import create_app
import os

# Print or log connection parameters
print("DB_HOST:", os.getenv('DB_HOST'))
print("DB_PORT:", os.getenv('DB_PORT'))
print("DB_USER:", os.getenv('DB_USER'))
print("DB_PASSWORD:", os.getenv('DB_PASSWORD'))
print("DB_NAME:", os.getenv('DB_NAME'))

# Create the Flask app
app = create_app()

# Define routes
@app.route('/')
def index():
    return "Welcome to the my_social_media_network app!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)