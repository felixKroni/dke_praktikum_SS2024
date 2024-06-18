from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from sqlalchemy.ext.declarative import AbstractConcreteBase
from sqlalchemy.orm import configure_mappers

from app import login

from app import db

wartung_mitarbeiter = db.Table(
    'wartung_mitarbeiter',
    db.Column('wartung_nr', db.String, db.ForeignKey('wartung.wartung_nr', ondelete='CASCADE'), nullable=False, primary_key=True),
    db.Column('mitarbeiter_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, primary_key=True)
)

class User(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True}
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    is_admin: so.Mapped[Optional[bool]] = so.mapped_column(sa.Boolean)


    def set_role(self, role):
        self.role = role


    def set_role(self, role):
        self.role = role

    def set_admin(self, is_admin):
        self.is_admin = is_admin


    def set_role(self, is_admin):
        self.role = is_admin

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login.user_loader
    def load_user(id):
        return db.session.get(User, int(id))

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Wagen(db.Model, AbstractConcreteBase):
    __table_args__ = {'extend_existing': True}
    wagennummer = db.Column(db.String, primary_key=True)
    spurweite = db.Column(db.Integer, index=True, nullable=False)

    def __repr__(self):
        return '<Wagen-Nr.: {}>'.format(self.wagennummer)



class Triebwagen(Wagen):
    __tablename__ = 'triebwagen'
    maxZugkraft = db.Column(db.Integer, nullable=False)
    zug = db.relationship('Zug', backref='triebwagen', uselist=False, cascade='all, delete')

    __mapper_args__ = {'polymorphic_identity': 'triebwagen', 'concrete': True}

    def __repr__(self):
        return '<Triebwagen-Nr.: {}>'.format(self.wagennummer)



class Personenwagen(Wagen):
    __tablename__ = 'personenwagen'
    sitzanzahl = db.Column(db.Integer, nullable=False)
    maximalgewicht = db.Column(db.Integer, nullable=False)

    __mapper_args__ = {'polymorphic_identity': 'personenwagen', 'concrete': True}
    zug_nummer = db.Column(db.String(255), db.ForeignKey('zug.zug_nummer', onupdate='CASCADE', ondelete='CASCADE'))

    def __repr__(self):
        return '<Personenwagen-Nr.: {}>'.format(self.wagennummer)


class Zug(db.Model):
    __table_args__ = {'extend_existing': True}
    zug_nummer = db.Column(db.String, primary_key=True)
    zug_name = db.Column(db.String, nullable=False)
    triebwagen_nr = db.Column(db.Integer, db.ForeignKey('triebwagen.wagennummer', onupdate='CASCADE', ondelete='CASCADE'),
                              unique=True, nullable=False)
    personenwagen = db.relationship('Personenwagen', backref='zug', lazy='dynamic')

    wartungen = db.relationship('Wartung', back_populates='zug', lazy='dynamic')

    def __repr__(self):
        return '<Zugnummer: {}>'.format(self.zug_nummer)


class Wartung(db.Model):
    __table_args__ = (sa.UniqueConstraint('start_time', name='uq_mitarbeiter_time'), {'extend_existing': True})
    wartung_nr = db.Column(db.String, primary_key=True)
    zug_nummer = db.Column(db.String, db.ForeignKey('zug.zug_nummer', ondelete='CASCADE'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    mitarbeiters = db.relationship("User", secondary=wartung_mitarbeiter, backref='wartungs', lazy=True)
    zug = db.relationship("Zug", back_populates="wartungen")

    def __repr__(self):
        return '<Wartung: Wartung-Nr {}, Mitarbeiters {}, Zugnummer {}, Start: {}, End: {}>'.format(
            self.wartung_nr, self.mitarbeiters, self.zug_nummer, self.start_time, self.end_time)
