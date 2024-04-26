from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.commons import Base


class MitarbeiterDurchfuehrung(Base):
    __tablename__ = 'Mitarbeiterdurchfuehrung'
    fahrtdurchfuehrung_id = Column(Integer, ForeignKey('Fahrtdurchfuehrung.id'), primary_key=True)
    mitarbeiter_id = Column(Integer, ForeignKey('Mitarbeiter.id'), primary_key=True)
    startZeit = Column(DateTime)  # The start time at which the employee is active

    fahrtdurchfuehrung = relationship("Fahrtdurchfuehrung", back_populates="mitarbeiter")
    mitarbeiter = relationship("Mitarbeiter", backref="fahrtdurchfuehrungen")