from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Fahrplan(Base):
    __tablename__ = 'fahrplan'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    zug = relationship("Zug", back_populates="fahrplan")