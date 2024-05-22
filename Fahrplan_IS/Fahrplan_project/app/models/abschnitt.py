from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import relationship

from app.commons import Base
from app.models.abschnitt_halteplan import AbschnittHalteplan


class Abschnitt(Base):
    __tablename__ = 'Abschnitt'
    id = Column(Integer, primary_key=True)
    spurenweite = Column(Float)
    nutzungsentgelt = Column(Float)
    StartBahnhof = Column(String)
    EndBahnhof = Column(String)
    halteplaene = relationship("AbschnittHalteplan", order_by=AbschnittHalteplan.reihung, back_populates="abschnitt")


