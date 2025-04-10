import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}
    MODEL_PATH = 'models/resume-classifier'
    API_VERSION = '1.0.0'
    API_TITLE = 'Resume Classifier API'
