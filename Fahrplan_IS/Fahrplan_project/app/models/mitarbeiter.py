from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, Enum
from sqlalchemy.orm import relationship
from app.database import Base, zugeteiltermitarbeiter_association


class Mitarbeiter(Base):
    __tablename__ = 'mitarbeiter'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    svnr = Column(String)
    username = Column(String)
    password = Column(String)
    rolle = Column(String)
    zugeteilte_zuege = relationship("Zug", secondary=zugeteiltermitarbeiter_association, backref="mitarbeiter")
