import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "beginner-secret-key-change-later")
    MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
    MYSQL_USER = os.getenv("MYSQL_USER", "flask_user")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "flask_password")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "library_db")
