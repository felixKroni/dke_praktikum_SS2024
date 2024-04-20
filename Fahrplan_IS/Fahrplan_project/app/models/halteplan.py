
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.abschnitt_halteplan import AbschnittHalteplan


class Halteplan(Base):
    __tablename__ = 'halteplan'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    streckenName = Column(String)
    abschnitte = relationship("AbschnittHalteplan", order_by=AbschnittHalteplan.reihung)
