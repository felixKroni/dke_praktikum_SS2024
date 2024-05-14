
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship
from app.commons import Base


class Fahrtdurchfuehrung(Base):
    __tablename__ = 'Fahrtdurchfuehrung'
    id = Column(Integer, primary_key=True)
    startZeit = Column(String)
    tag = Column(Date)
    ausfall = Column(Boolean)
    verspaetung = Column(Boolean)
    preis = Column(Float)
    zug_id = Column(Integer, ForeignKey('Zug.id'))
    zug = relationship("Zug", back_populates="fahrtdurchfuehrungen")
    mitarbeiter = relationship("MitarbeiterDurchfuehrung", back_populates="fahrtdurchfuehrung")