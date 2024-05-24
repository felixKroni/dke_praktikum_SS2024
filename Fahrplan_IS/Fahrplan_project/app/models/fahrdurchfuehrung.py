
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, Date, DateTime
from sqlalchemy.orm import relationship
from app.commons import Base


class Fahrtdurchfuehrung(Base):
    __tablename__ = 'Fahrtdurchfuehrung'
    id = Column(Integer, primary_key=True)
    startZeit = Column(DateTime)
    ausfall = Column(Boolean)
    verspaetung = Column(Boolean)
    preis = Column(Float)
    zug_id = Column(Integer, ForeignKey('Zug.id'))
    zug = relationship("Zug", back_populates="fahrtdurchfuehrungen")
    mitarbeiter = relationship("MitarbeiterDurchfuehrung", back_populates="fahrtdurchfuehrung")
    fahrplan_id = Column(Integer, ForeignKey('Fahrplan.id'))