from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, Enum


from app.commons import Base
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Mitarbeiter(Base, UserMixin):
    __tablename__ = 'Mitarbeiter'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    svnr = Column(String)
    email = Column(String)
    username = Column(String)
    password = Column(String)
    role = Column(String)


    def __repr__(self):
        return '<User {}>'.format(self.name)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)




