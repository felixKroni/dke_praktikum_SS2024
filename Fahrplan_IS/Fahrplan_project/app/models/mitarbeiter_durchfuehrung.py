from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base


class MitarbeiterDurchfuehrung(Base):
    __tablename__ = 'mitarbeiterdurchfuehrung'
    fahrtdurchführung_id = Column(Integer, ForeignKey('fahrtdurchfuehrung.id'), primary_key=True)
    mitarbeiter_id = Column(Integer, ForeignKey('mitarbeiter.id'), primary_key=True)
    startZeit = Column(DateTime)  # The start time at which the employee is active

    fahrtdurchführung = relationship("Fahrtdurchführung", back_populates="mitarbeiter")
    mitarbeiter = relationship("Mitarbeiter", back_populates="fahrtdurchfuehrungen")