import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:rahasia@localhost:5432/hmrecord'  # Update with your DB credentials
    SQLALCHEMY_TRACK_MODIFICATIONS = False