import os
from dotenv import load_dotenv
load_dotenv()
ZOOM_API_KEY = os.getenv('ZOOM_API_KEY')
ZOOM_API_SECRET = os.getenv('ZOOM_API_SECRET')
SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-here')