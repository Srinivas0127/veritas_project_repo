# Veritas Configuration File
# Environment settings and application configuration

import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'veritas-news-analysis-2026-dev-key'
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    # Server settings
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    # AI Model settings
    AI_MODEL_CACHE_DIR = os.environ.get('AI_MODEL_CACHE_DIR', './models')
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 10000))  # characters
    
    # Web scraping settings
    SCRAPING_TIMEOUT = int(os.environ.get('SCRAPING_TIMEOUT', 30))  # seconds
    USER_AGENT = os.environ.get('USER_AGENT', 
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    
    # Rate limiting (if needed)
    RATELIMIT_ENABLED = os.environ.get('RATELIMIT_ENABLED', 'False').lower() == 'true'
    REQUESTS_PER_MINUTE = int(os.environ.get('REQUESTS_PER_MINUTE', 60))
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')  # Must be set in production
    
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable must be set in production")

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}