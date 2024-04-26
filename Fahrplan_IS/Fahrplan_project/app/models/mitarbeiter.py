from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, Enum
from sqlalchemy.orm import relationship
from app.commons import Base


class Mitarbeiter(Base):
    __tablename__ = 'Mitarbeiter'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    svnr = Column(String)
    username = Column(String)
    password = Column(String)
    rolle = Column(String)

    def __repr__(self):
        return '<User {}>'.format(self.username)