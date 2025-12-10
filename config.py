"""config.py - simple config"""
import os
class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET", "please-change-me-for-prod")
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATABASE = os.path.join(BASE_DIR, "library.db")
