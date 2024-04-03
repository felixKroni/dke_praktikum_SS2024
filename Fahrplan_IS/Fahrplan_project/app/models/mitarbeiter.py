from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from app.models.role import Role

Base = declarative_base()


class Mitarbeiter(Base):
    __tablename__ = 'mitarbeiter'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    role = Column(Enum(Role))  # Neue Rolle Spalte
    fahrtdurchfuehrungen = relationship('Fahrtdurchfuerung', secondary='mitarbeiter_fahrtdurchfuerung', backref='mitarbeiter')

mitarbeiter_fahrtdurchfuerung = Table('mitarbeiter_fahrtdurchfuerung', Base.metadata,
    Column('mitarbeiter_id', Integer, ForeignKey('mitarbeiter.id')),
    Column('fahrtdurchfuerung_id', Integer, ForeignKey('fahrtdurchfuerung.id'))
)