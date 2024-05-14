from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, backref
from app.commons import Base


class AbschnittHalteplan(Base):
    __tablename__ = 'Abschnitt_halteplan'
    abschnitt_id = Column(Integer, ForeignKey('Abschnitt.id'), primary_key=True)
    halteplan_id = Column(Integer, ForeignKey('Halteplan.id'), primary_key=True)
    reihung = Column(Integer)
    # möglicherweise backpopulates verwenden statt backref
    abschnitt = relationship("Abschnitt", back_populates="halteplaene")
    halteplan = relationship("Halteplan", back_populates="abschnitte")
