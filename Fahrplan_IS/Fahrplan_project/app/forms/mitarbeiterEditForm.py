from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError

from app import database


class MitarbeiterEditForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    svnr = StringField('SVNR', validators=[DataRequired()])
    role = SelectField('Rolle auswählen', choices=[('admin', 'Administrator'), ('ma', 'Mitarbeiter')], validators=[DataRequired()])
    username = StringField('Benutzername', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    password2 = PasswordField(
        'Passwort wiederholen', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Edit')
