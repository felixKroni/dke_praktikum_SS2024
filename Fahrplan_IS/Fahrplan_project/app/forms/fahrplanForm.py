from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, DateField
from wtforms.fields.choices import SelectField
from wtforms.fields.datetime import TimeField
from wtforms.fields.form import FormField
from wtforms.fields.list import FieldList
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, ValidationError, Optional


class FahrplanForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    gueltig_von = DateField('Gültig von', validators=[DataRequired()])
    gueltig_bis = DateField('Gültig bis', validators=[DataRequired()])
    halteplan_selection = SelectField('zugehörigen Halteplan auswählen', choices=[], validators=[DataRequired()])
    choice = SelectField('Typ wählen', choices=[('specific', 'Spezifische Tage'), ('weekly', 'Wochentage')], validators=[DataRequired()])
    submit = SubmitField('Fahrplan Erstellen')


class TimeSpecificationForm(FlaskForm):
    specific_times = StringField('Spezifische Zeiten', validators=[DataRequired()])
    time_range_start = TimeField('Startzeit', validators=[DataRequired()])
    time_range_end = TimeField('Endzeit', validators=[DataRequired()])
    interval = IntegerField('Intervall in Stunden', validators=[DataRequired()])
    submit = SubmitField('Fahrplan Erstellen')


class TimeInputForm(FlaskForm):
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[Optional()])
    interval = StringField('Interval in Stunden(2 = alle 2 Stunden)')
    submit = SubmitField('Bestätigen')

    def validate_start_time(form, field):
        if form.end_time.data is not None and form.start_time.data > form.end_time.data:
            raise ValidationError('Start time must be before end time')

class SpecificDateForm(FlaskForm):
    date = DateField('Datum', validators=[DataRequired()])
    time = FormField(TimeInputForm)
    submit = SubmitField('Speichern und Abschließen')
    new = SubmitField('Speichern und neue Zeit hinzufügen')

    def validate_date(form, field):
        if form.gueltig_von and form.gueltig_bis:
            if not (form.gueltig_von.date() <= field.data <= form.gueltig_bis.date()):
                raise ValidationError(f'Datum muss im Fahrplan Gültigkeitsbreich zwischen {form.gueltig_von.date()} und {form.gueltig_bis.date()} liegen.')

class WeeklyDaysForm(FlaskForm):
    weekdays = SelectField('Weekdays', choices=[('montag', 'Montag'), ('' 'dienstag', 'Dienstag'), ('mittwoch', 'Mittwoch'), ('donnerstag', 'Donnerstag'), ('freitag', 'Freitag'), ('samstag', 'Samstag'), ('sonntag', 'Sonntag')], validators=[DataRequired()])
    time = FormField(TimeInputForm)
    submit = SubmitField('Speichern und Abschließen')
    new = SubmitField('Speichern und neue Zeit hinzufügen')


class ConfirmFahrplanForm(FlaskForm):
    fahrplan = []
    submit = SubmitField('Confirm')

