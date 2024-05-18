
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, Length, ValidationError
from wtforms.fields.choices import SelectMultipleField

class HalteplanCreateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    streckenName = SelectField('Strecken Name', choices=[], validators=[DataRequired()])
    submit = SubmitField('Create Halteplan')





class HalteplanChooseHaltepunktForm(FlaskForm):
    haltepunkte = SelectMultipleField('Haltepunkte', choices=[], validators=[DataRequired()])

    submit = SubmitField('Choose Haltepunkte')


    def validate_haltepunkte(self, haltepunkte):
        if len(haltepunkte.data) < 2:
            raise ValidationError('Please select at least 2 Haltepunkte.')