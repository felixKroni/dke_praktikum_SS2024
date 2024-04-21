from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, Enum
from sqlalchemy.orm import relationship
from app.commons import Base


class Zug(Base):
    __tablename__ = 'zug'
    id = Column(Integer, primary_key=True)
    spurenweite = Column(Float)
    name = Column(String)
    fahrplan_id = Column(Integer, ForeignKey('fahrplan.id'))
    fahrplan = relationship("Fahrplan", back_populates="zug")
    fahrtdurchfuehrungen = relationship("Fahrtdurchführung", back_populates="zug")