
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Halteplan(Base):
    __tablename__ = 'halteplan'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    haltepunkte = relationship('Haltepunkt', backref='halteplan')
    preis = Column(Float)
    fahrplan_id = Column(Integer, ForeignKey('fahrplan.id'))
    fahrplan = relationship('Fahrplan', backref='halteplan')