from pathlib import Path

from flask import Flask
from .config import Config
from .database import Database
from flask_login import LoginManager

db_path = Path('.') / 'app' / 'data' / 'database.db'
database = Database(db_path)
app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
login.login_view = 'login'

from app import routes

@login.user_loader
def load_user(id):
    from app.models.mitarbeiter import Mitarbeiter
    return database.baseController.find_by_id(Mitarbeiter, id)
