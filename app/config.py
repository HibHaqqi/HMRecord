import os

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:rahasia@localhost:5432/hmrecord'
    SQLALCHEMY_TRACK_MODIFICATIONS = False