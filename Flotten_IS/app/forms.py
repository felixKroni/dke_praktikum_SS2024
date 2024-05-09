from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, FloatField, IntegerField, \
    DateField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
import sqlalchemy as sa
from app import db
from app.models import User, Triebwagen, Personenwagen, Wagen, Zug


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


class TriebwagenForm(FlaskForm):
    wagennummer = StringField('Wagennummer', validators=[DataRequired(), Length(min=5, max=10)])
    spurweite = SelectField('Spurweite', choices=[('1435', 'Normalspur (1435 mm)'), ('1000', 'Schmalspur (1000 mm)')], validators=[DataRequired()])
    maxZugkraft = StringField('Maximale Zugkraft [Tonnen]', validators=[DataRequired(), Length(max=3)])
    submit = SubmitField('Speichern')

    def validate_wagennummer(self, wagennummer):
        for character in wagennummer.data:
            wagen = Wagen.query.filter_by(wagennummer=wagennummer.data).first()
            if wagen is not None:
                raise ValidationError('Diese Wagennummer wurde bereits verwendet!')

    def validate_maxZugkraft(self, maxZugkraft):
        for character in maxZugkraft.data:
            if not character.isdigit():
                raise ValidationError('Die maximale Zugkraft muss nur aus Zahlen bestehen!')



class PersonenwagenForm(FlaskForm):
    wagennummer = StringField('Wagennummer', validators=[DataRequired(), Length(min=5, max=12)])
    spurweite = SelectField('Spurweite', choices=[('1435', 'Normalspur (1435 mm)'), ('1000', 'Schmalspur (1000 mm)')], validators=[DataRequired()])
    sitzanzahl = StringField('Sitzanzahl', validators=[DataRequired(), Length(max=2)])
    maximalgewicht = StringField('Maximalgewicht [Tonnen]', validators=[DataRequired(), Length(max=3)])
    submit = SubmitField('Speichern')

    def validate_wagennummer(self, wagennummer):
        for character in wagennummer.data:
            wagen = Wagen.query.filter_by(wagennummer=wagennummer.data).first()
            if wagen is not None:
                raise ValidationError('Diese Wagennummer wurde bereits verwendet!')

    def validate_sitzanzahl(self, sitzanzahl):
        for character in sitzanzahl.data:
            if not character.isdigit():
                raise ValidationError('Die Sitzanzahl muss nur aus Zahlen bestehen!!')

    def validate_maximalgewicht(self, maximalgewicht):
        for character in maximalgewicht.data:
            if not character.isdigit():
                raise ValidationError('Das Maximalgewicht muss nur aus Zahlen bestehen!!')



class UpdateTriebwagenForm(FlaskForm):
    wagennummer = StringField('Wagennummer', validators=[DataRequired(), Length(min=5, max=10)])
    spurweite = SelectField('Spurweite', choices=[('1435', 'Normalspur (1435 mm)'), ('1000', 'Schmalspur (1000 mm)')],
                            validators=[DataRequired()])
    maxZugkraft = StringField('Maximale Zugkraft [Tonnen]', validators=[DataRequired(), Length(max=3)])
    submit = SubmitField('Speichern')

    def __init__(self, original_wagennummer, *args, **kwargs):
        super(UpdateTriebwagenForm, self).__init__(*args, **kwargs)
        self.original_wagennummer = original_wagennummer

    def validate_wagennummer(self, wagennummer):
        for character in wagennummer.data:
            if str(wagennummer.data) != self.original_wagennummer:
                wagen = Wagen.query.filter_by(wagennummer=wagennummer.data).first()
                if wagen is not None:
                    raise ValidationError('Diese Wagennummer wurde bereits verwendet!')

    def validate_maxZugkraft(self, maxZugkraft):
        for character in maxZugkraft.data:
            if not character.isdigit():
                raise ValidationError('Die maximale Zugkraft muss nur aus Zahlen bestehen!')



class UpdatePersonenwagenForm(FlaskForm):
    wagennummer = StringField('Wagennummer', validators=[DataRequired(), Length(min=5, max=10)])
    spurweite = SelectField('Spurweite', choices=[('1435', 'Normalspur (1435 mm)'), ('1000', 'Schmalspur (1000 mm)')], validators=[DataRequired()])
    sitzanzahl = StringField('Sitzanzahl', validators=[DataRequired(), Length(max=3)])
    maximalgewicht = StringField('Maximalgewicht [Tonnen]', validators=[DataRequired(), Length(max=3)])
    submit = SubmitField('Speichern')

    def __init__(self, original_wagennummer, *args, **kwargs):
        super(UpdatePersonenwagenForm, self).__init__(*args, **kwargs)
        self.original_wagennummer = original_wagennummer


    def validate_nr(self, wagennummer):
        for character in wagennummer.data:
            if str(wagennummer.data) != self.original_wagennummer:
                wagen = Wagen.query.filter_by(wagennummer=wagennummer.data).first()
                if wagen is not None:
                    raise ValidationError('Diese Wagennummer wurde bereits verwendet!')

    def validate_sitzanzahl(self, sitzanzahl):
        for character in sitzanzahl.data:
            if not character.isdigit():
                raise ValidationError('Die Sitzanzahl muss nur aus Zahlen bestehen!')

    def validate_maximalgewicht(self, maximalgewicht):
        for character in maximalgewicht.data:
            if not character.isdigit():
                raise ValidationError('Das Maximalgewicht muss nur aus Zahlen bestehen!')

class ZugForm(FlaskForm):
    zug_nummer = StringField('Zugnummer', validators=[DataRequired(), Length(min=5, max=10)])
    zug_name = StringField('Zugname', validators=[DataRequired()])
    triebwagen_nr = SelectField('Triebwagen', validators=[DataRequired()])
    submit = SubmitField('Speichern')

    def validate_nr(self, zug_nummer):
        zug = Zug.query.filter_by(zug_nummer=zug_nummer.data).first()
        if zug is not None:
            raise ValidationError('Diese Zugnummer wurde bereits verwendet!')


class UpdateZugForm(FlaskForm):
    zug_nummer = StringField('Zugnummer', validators=[DataRequired(), Length(min=5, max=10)])
    zug_name = StringField('Zugname', validators=[DataRequired()])
    triebwagen_nr = SelectField('Triebwagen', validators=[DataRequired()])
    submit = SubmitField('Speichern')

    def __init__(self, original_zug_nummer, original_triebwagen_nr, *args, **kwargs):
        super(UpdateZugForm, self).__init__(*args, **kwargs)
        self.original_zug_nummer = original_zug_nummer
        self.original_triebwagen_nr = original_triebwagen_nr

    def validate_nr(self, zug_nummer):
        if zug_nummer.data != self.original_zug_nummer:
            zug = Zug.query.filter_by(zug_nummer=zug_nummer.data).first()
            if zug is not None:
                raise ValidationError('Diese Zugnummer wurde bereits verwendet!')

    def validate_triebwagen_nr(self, triebwagen_nr):
        if triebwagen_nr.data != self.original_triebwagen_nr:
            triebwagen = Triebwagen.query.filter_by(wagennummer=triebwagen_nr.data).first()
            if triebwagen.zug is not None and triebwagen.zug.wagennummer != self.original_nr:
                raise ValidationError('Diese Wagennummer wurde bereits verwendet!')








