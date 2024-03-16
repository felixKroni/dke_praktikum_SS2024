from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String, Date, Float
from app import db
from app import login

class User(UserMixin, db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    email = Column(String(120), index=True, unique=True)
    password_hash = Column(String(256))
    role = Column(String(64))

    def set_role(self, role):
        self.role = role

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    @login.user_loader
    def load_user(id):
        return db.session.get(User, int(id))

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Bahnhof(db.Model):
    name = Column(String(64), primary_key=True)
    adresse = Column(String(256))
    latitude = Column(Float)
    longitude = Column(Float)

    def __repr__(self):
        return '<Bahnhof {}>'.format(self.name)
