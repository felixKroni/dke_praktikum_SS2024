from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, DateField
from wtforms.fields.choices import SelectField
from wtforms.fields.datetime import TimeField
from wtforms.fields.form import FormField
from wtforms.fields.list import FieldList
from wtforms.fields.numeric import IntegerField, FloatField
from wtforms.validators import DataRequired, ValidationError, Optional


class FahrplanForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    gueltig_von = DateField('Gültig von', validators=[DataRequired()])
    gueltig_bis = DateField('Gültig bis', validators=[DataRequired()])
    halteplan_selection = SelectField('zugehörigen Halteplan auswählen', choices=[], validators=[DataRequired()])
    choice = SelectField('Typ wählen', choices=[('specific', 'Spezifische Tage'), ('weekly', 'Wochentage')],
                         validators=[DataRequired()])
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
    interval = IntegerField('Interval in Stunden(2 = alle 2 Stunden)')
    submit = SubmitField('Bestätigen')

    def validate_start_time(form, field):
        if form.end_time.data is not None and field.data > form.end_time.data:
            raise ValidationError('Startzeit muss vor der Endzeit liegen.')

    def validate_interval(form, field):
        if field.data is not None and field.data < 1:
            raise ValidationError('Interval muss größer als 0 sein')
        if field.data is not None and field.data > 24:
            raise ValidationError('Interval muss kleiner als 24 sein')
        if form.end_time.data is not None and field is None:
            raise ValidationError('Interval muss angegeben werden, wenn eine Endzeit angegeben ist.')


class SpecificDateForm(FlaskForm):
    date = DateField('Datum', validators=[DataRequired()])
    time = FormField(TimeInputForm)
    submit = SubmitField('Speichern und Abschließen')
    new = SubmitField('Speichern und neue Zeit hinzufügen')
    specialPrices = SubmitField('Sonderpreise festlegen')

    def set_time_data(self, start_time, end_time, interval):
        self.time.start_time.data = datetime.strptime(start_time, '%H:%M:%S').time()
        self.time.end_time.data = datetime.strptime(end_time, '%H:%M:%S').time()
        self.time.interval.data = interval

    def validate_date(form, field):
        if form.gueltig_von and form.gueltig_bis:
            if not (form.gueltig_von.date() <= field.data <= form.gueltig_bis.date()):
                raise ValidationError(
                    f'Datum muss im Fahrplan Gültigkeitsbreich zwischen {form.gueltig_von.date()} und {form.gueltig_bis.date()} liegen.')


class WeeklyDaysForm(FlaskForm):
    weekdays = SelectField('Weekdays',
                           choices=[('montag', 'Montag'), ('' 'dienstag', 'Dienstag'), ('mittwoch', 'Mittwoch'),
                                    ('donnerstag', 'Donnerstag'), ('freitag', 'Freitag'), ('samstag', 'Samstag'),
                                    ('sonntag', 'Sonntag')], validators=[DataRequired()])
    time = FormField(TimeInputForm)
    submit = SubmitField('Speichern und Abschließen')
    new = SubmitField('Speichern und neue Zeit hinzufügen')
    specialPrices = SubmitField('Sonderpreise festlegen')

    def set_time_data(self, start_time, end_time, interval):
        self.time.start_time.data = datetime.strptime(start_time, '%H:%M:%S').time()
        self.time.end_time.data = datetime.strptime(end_time, '%H:%M:%S').time()
        self.time.interval.data = interval


class SpecialPricesForm(FlaskForm):
    price_multiplier = FloatField('Preisfaktor', validators=[DataRequired()], default=1.0, render_kw={'step': '0.01'})
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired()])
    submit = SubmitField('Speichern')

    def validate_start_time(form, field):
        if field.data > form.end_time.data:
            raise ValidationError('Startzeit muss vor der Endzeit liegen.')
        if field.data < form.weeklyDay_start_time:
            raise ValidationError('Startzeit muss nach der Startzeit des Wochentags liegen.')
        if form.weeklyDay_end_time is not None and field.data > form.weeklyDay_end_time:
            raise ValidationError('Startzeit muss vor der Endzeit des Wochentags liegen.')

    def validate_end_time(form, field):
        if field.data < form.start_time.data:
            raise ValidationError('Endzeit muss nach der Startzeit liegen.')
        if form.weeklyDay_end_time is not None and field.data > form.weeklyDay_end_time:
            raise ValidationError('Endzeit muss vor der Endzeit des Wochentags liegen.')
        if field.data < form.weeklyDay_start_time:
            raise ValidationError('Endzeit muss nach der Startzeit des Wochentags liegen.')


class ConfirmFahrplanForm(FlaskForm):
    fahrplan = []
    submit = SubmitField('Bestätigen')
    revoke = SubmitField('Alles Zurücksetzen')
