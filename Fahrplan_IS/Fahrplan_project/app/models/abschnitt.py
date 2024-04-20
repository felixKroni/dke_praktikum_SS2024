from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.abschnitt_halteplan import AbschnittHalteplan


class Abschnitt(Base):
    __tablename__ = 'abschnitt'
    id = Column(Integer, primary_key=True)
    spurenweite = Column(Float)
    nutzungsentgeld = Column(Float)
    StartBahnhof = Column(String)
    EndBahnhof = Column(String)
    halteplaene = relationship("AbschnittHalteplan", order_by=AbschnittHalteplan.reihung)


