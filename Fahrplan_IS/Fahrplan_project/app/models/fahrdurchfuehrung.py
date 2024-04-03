
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Fahrtdurchfuerung(Base):
    __tablename__ = 'fahrtdurchfuerung'

    id = Column(Integer, primary_key=True)
    zug_id = Column(Integer, ForeignKey('zug.id'))  # Zug, der die Fahrt durchführt
    zug = relationship('Zug', backref='fahrtdurchfuerungen')
    verspaetung = Column(Integer, default=0)  # Verspätung in Minuten
    ausgefallen = Column(Boolean, default=False)  # Ob die Fahrtdurchführung ausfällt
    preis = Column(Float)  # Preis für Fahrten zu bestimmten Zeitpunkten
    fahrplan_id = Column(Integer, ForeignKey('fahrplan.id'))  # Zugehöriger Fahrplan
    fahrplan = relationship('Fahrplan', backref='fahrtdurchfuerungen')
    mitarbeiter = relationship('Mitarbeiter', secondary='mitarbeiter_fahrtdurchfuerung', backref='fahrtdurchfuerungen')  # Mitarbeiter, die der Fahrtdurchführung zugeordnet sind