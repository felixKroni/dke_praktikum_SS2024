from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()



class Fahrplan(Base):
    __tablename__ = 'fahrplan'

    id = Column(Integer, primary_key=True)
    fahrplanname = Column(String)
    Zeitintervall = Column(String)
    fahrtdurchfuehrungen = relationship('Fahrtdurchfuerung', backref='fahrplan')