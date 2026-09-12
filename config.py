import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'csv'}
    DATABASE_PATH = 'database.db'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))