from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, backref
from app.commons import Base


class AbschnittHalteplan(Base):
    __tablename__ = 'abschnitt_halteplan'
    abschnitt_id = Column(Integer, ForeignKey('abschnitt.id'), primary_key=True)
    halteplan_id = Column(Integer, ForeignKey('halteplan.id'), primary_key=True)
    reihung = Column(Integer)  # This column is used to determine the order

    # Relationship backrefs
    abschnitt = relationship("Abschnitt", backref=backref("halteplan_associations"))
    halteplan = relationship("Halteplan", backref=backref("abschnitt_associations"))
