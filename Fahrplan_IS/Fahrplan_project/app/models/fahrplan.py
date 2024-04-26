from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.commons import Base


class Fahrplan(Base):
    __tablename__ = 'Fahrplan'
    id = Column(Integer, primary_key=True)
    name = Column(String)