from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, ForeignKeyConstraint
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

class Abschnitt(db.Model):
    abschnitt_id = Column(Integer, primary_key=True)
    startbahnhof_id = Column(String(64), ForeignKey('bahnhof.name'))
    endbahnhof_id = Column(String(64), ForeignKey('bahnhof.name'))
    strecke_id = Column(String(64), ForeignKey('strecke.name'))
    maximale_geschwindigkeit = Column(Integer)
    maximale_spurweite = Column(Integer)
    nutzungsentgelt = Column(Integer)
    distanz = Column(Integer)
    warnung = db.Column(db.Boolean)
    startbahnhof = relationship('Bahnhof', foreign_keys=[startbahnhof_id])
    endbahnhof = relationship('Bahnhof', foreign_keys=[endbahnhof_id])
    strecke = relationship('Strecke', foreign_keys=[strecke_id])

    def __repr__(self):
        return '<Abschnitt {}-{}>'.format(self.startbahnhof_id, self.endbahnhof_id)

class Warnung(db.Model):
    warnung_id = Column(Integer, primary_key=True)
    titel = Column(String(64))
    gueltigkeitsdatum = Column(Date)
    beschreibung = Column(String(256))
    abschnitt_id_warnung = Column(Integer, ForeignKey('abschnitt.abschnitt_id'))
    abschnitt = relationship('Abschnitt', foreign_keys=[abschnitt_id_warnung])

    def __repr__(self):
        return '<Warnung {}>'.format(self.warnung_id)

class Strecke(db.Model):
    name = db.Column(db.String(64), primary_key=True)
    #abschnitte = relationship('Abschnitt', backref='strecke')

    def __repr__(self):
        return '<Strecke {}>'.format(self.name)
