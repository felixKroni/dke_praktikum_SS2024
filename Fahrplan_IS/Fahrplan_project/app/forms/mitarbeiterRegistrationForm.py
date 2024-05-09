from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError

from app import database


class MitarbeiterRegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    svnr = StringField('SVNR', validators=[DataRequired()])
    role = StringField('Role', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Passwort wiederholen', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrieren')

    def validate_username(self, username):
        user = database.get_controller('ma').get_mitarbeiter_by_username(username.data)
        if user is not None:
            raise ValidationError('Bitte benutze einen anderen Benutzernamen.')

    def validate_email(self, email):
        user = database.get_controller('ma').get_mitarbeiter_by_email(email.data)
        if user is not None:
            raise ValidationError('Bitte benutze eine andere Email-Adresse.')