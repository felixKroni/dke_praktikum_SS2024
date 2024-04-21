from pathlib import Path

from flask import Flask
from .config import Config
from .database import init_db

db_path = Path('.') / 'app' / 'data' / 'database.db'
init_db(db_path)
app = Flask(__name__)
app.config.from_object(Config)

from app import routes
