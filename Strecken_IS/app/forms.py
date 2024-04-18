from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, FloatField, IntegerField, \
    DateField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import sqlalchemy as sa
from app import db
from app.models import User
from app.models import Bahnhof
from app.models import Abschnitt
from app.models import Strecke


def get_bahnhof_choices():
    return [(b.name, b.name) for b in Bahnhof.query.all()]


def get_abschnitt_choices():
    return [(a.abschnitt_id, f"{a.startbahnhof_id}-{a.endbahnhof_id}") for a in Abschnitt.query.all()]


def get_strecke_choices():
    return [(s.name, s.name) for s in Strecke.query.all()]


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('admin', 'Admin'), ('user', 'User')], validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')


class BahnhofForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    adresse = StringField('Adresse', validators=[DataRequired()])
    latitude = FloatField('Latitude', validators=[DataRequired()])
    longitude = FloatField('Longitude', validators=[DataRequired()])
    submit = SubmitField('Submit')


class AbschnittForm(FlaskForm):
    startbahnhof_id = SelectField('Startbahnhof', choices=get_bahnhof_choices, validators=[DataRequired()])
    endbahnhof_id = SelectField('Endbahnhof', choices=get_bahnhof_choices, validators=[DataRequired()])
    strecke_id = SelectField('Strecke', choices=get_strecke_choices, validators=[DataRequired()])
    maximale_geschwindigkeit = IntegerField('Maximale Geschwindigkeit [km/h]', validators=[DataRequired()])
    maximale_spurweite = SelectField('Maximale Spurweite [cm]', choices=[(140, '140'), (120, '120')], coerce=int, validators=[DataRequired()])
    nutzungsentgelt = IntegerField('Nutzungsentgelt [€]', validators=[DataRequired()])
    distanz = IntegerField('Distanz [km]', validators=[DataRequired()])
    submit = SubmitField('Submit')
    def validate_endbahnhof_id(self, endbahnhof_id):
        if endbahnhof_id.data == self.startbahnhof_id.data:
            raise ValidationError('Startbahnhof und Endbahnhof können nicht identisch sein.')


class WarnungForm(FlaskForm):
    abschnitt_id_warnung = SelectField('Abschnitt', choices=get_abschnitt_choices, validators=[DataRequired()])
    titel = StringField('Titel', validators=[DataRequired()])
    gueltigkeitsdatum = DateField('Gültigkeitsdatum', format='%Y-%m-%d', validators=[DataRequired()])
    beschreibung = TextAreaField('Beschreibung', validators=[DataRequired()])
    submit = SubmitField('Submit')


class StreckeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Speichern')
