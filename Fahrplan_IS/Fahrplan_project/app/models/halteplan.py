
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.commons import Base
from app.models.abschnitt_halteplan import AbschnittHalteplan


class Halteplan(Base):
    __tablename__ = 'Halteplan'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    streckenName = Column(String)
    abschnitte = relationship("AbschnittHalteplan", order_by=AbschnittHalteplan.reihung, back_populates="halteplan")
