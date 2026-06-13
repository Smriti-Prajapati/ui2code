"""
Configuration module for UI2CODE system
"""
import os

try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception:
    pass

class Config:
    """Base configuration"""
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.dirname(BASE_DIR)
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    # Upload
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', os.path.join(BASE_DIR, 'uploads'))
    OUTPUT_FOLDER = os.getenv('OUTPUT_FOLDER', os.path.join(PROJECT_ROOT, 'output'))
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 10485760))  # 10MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///ui2code.db')
    VECTOR_DB_PATH = os.getenv('VECTOR_DB_PATH', './vector_db')
    
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')
    
    # Model Paths
    YOLO_MODEL_PATH = os.getenv('YOLO_MODEL_PATH', os.path.join(PROJECT_ROOT, 'model', 'ui-yolov8.pt'))
    DETECTRON2_CONFIG = os.getenv('DETECTRON2_CONFIG', os.path.join(PROJECT_ROOT, 'model', 'detectron2_config.yaml'))
    
    # Code Generation
    DEFAULT_FRAMEWORK = os.getenv('DEFAULT_FRAMEWORK', 'react')
    DEFAULT_STYLING = os.getenv('DEFAULT_STYLING', 'tailwind')
    
    # Component Detection Classes
    UI_COMPONENTS = [
        'button', 'text', 'image', 'card', 'form', 'input',
        'navbar', 'sidebar', 'icon', 'container', 'table',
        'menu', 'header', 'footer', 'modal', 'dropdown',
        'checkbox', 'radio', 'slider', 'tabs', 'accordion'
    ]
    
    # Text Classification Categories
    TEXT_CATEGORIES = [
        'heading', 'subheading', 'paragraph', 'button_text',
        'menu_item', 'form_label', 'caption', 'link'
    ]
    
    @staticmethod
    def init_app(app):
        """Initialize application with config"""
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.OUTPUT_FOLDER, exist_ok=True)
        os.makedirs(os.path.join(Config.PROJECT_ROOT, 'model'), exist_ok=True)
        os.makedirs(os.path.join(Config.PROJECT_ROOT, 'dataset'), exist_ok=True)
