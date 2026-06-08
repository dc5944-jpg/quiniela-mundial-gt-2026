import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "quiniela-mundial-gt-2026")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///quiniela.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
