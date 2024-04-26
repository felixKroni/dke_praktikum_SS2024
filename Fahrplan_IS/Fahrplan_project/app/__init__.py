from pathlib import Path

from flask import Flask
from .config import Config
from .database import Database

db_path = Path('.') / 'app' / 'data' / 'database.db'
database = Database(db_path)
app = Flask(__name__)
app.config.from_object(Config)

from app import routes
