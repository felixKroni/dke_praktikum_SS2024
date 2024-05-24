from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from app.commons import Base


class Fahrplan(Base):
    __tablename__ = 'Fahrplan'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    gueltig_von = Column(DateTime)
    gueltig_bis = Column(DateTime)
    fahrtdurchfuehrungen = relationship('Fahrtdurchfuehrung', backref='fahrplan')
    halteplan_id = Column(Integer, ForeignKey('Halteplan.id'))
    halteplan = relationship("Halteplan", back_populates="fahrplan")