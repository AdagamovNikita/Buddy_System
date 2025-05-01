# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Zoom API Configuration
ZOOM_API_KEY = os.getenv('ZOOM_API_KEY')
ZOOM_API_SECRET = os.getenv('ZOOM_API_SECRET')

# Flask Configuration
SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-here')