from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, DateField
from wtforms.fields.choices import SelectField
from wtforms.fields.datetime import TimeField, DateTimeField
from wtforms.fields.form import FormField
from wtforms.fields.list import FieldList
from wtforms.fields.numeric import IntegerField, FloatField
from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired, ValidationError


class EditFahrtdurchfuehrungForm(FlaskForm):
    startZeit = DateTimeField('Startzeit', validators=[DataRequired()], render_kw={'readonly': True})
    ausfall = BooleanField('Ausfall')
    verspaetung = BooleanField('Verspätung')
    preis = FloatField('Gesamtpreis', validators=[DataRequired()])
    zug_selection = SelectField('Zug zuteilen', choices=[])
    mitarbeiter_selection = SelectMultipleField('Mitarbeiter zuteilen', choices=[])
    submit = SubmitField('Fahrtdurchführung speichern')


    def validate_preis(form, field):
        if round(field.data, 2) != field.data:
            raise ValidationError('Maximal 2 Nachkommastellen erlaubt')

        if field.data < 0:
            raise ValidationError('Preis muss positiv sein')