from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, Enum, Boolean
from sqlalchemy.orm import relationship
from app.commons import Base


class Zug(Base):
    __tablename__ = 'Zug'
    id = Column(Integer, primary_key=True)
    spurenweite = Column(Float)
    name = Column(String)
    fahrplan_id = Column(Integer, ForeignKey('Fahrplan.id'))
    reserviert = Column(Boolean)
    fahrtdurchfuehrungen = relationship("Fahrtdurchfuehrung", back_populates="zug")

    def __repr__(self):
        return 'ID: ' + str(self.id) + ' Name: ' + self.name + ' Spurenweite: '+ str(self.spurenweite)