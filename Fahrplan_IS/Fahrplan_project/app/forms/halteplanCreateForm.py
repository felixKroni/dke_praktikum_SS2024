
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, Length, ValidationError
from wtforms.fields.choices import SelectMultipleField

class HalteplanCreateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    streckenName = SelectField('Strecken Name', choices=[], validators=[DataRequired()])
    submit = SubmitField('Halteplan Erstellen')





class HalteplanChooseHaltepunktForm(FlaskForm):
    haltepunkte = SelectMultipleField('Haltepunkte', choices=[], validators=[DataRequired()])

    submit = SubmitField('Haltepunkte festlegen')


    def validate_haltepunkte(self, haltepunkte):
        if len(haltepunkte.data) < 2:
            raise ValidationError('Bitte zumindest zwei Haltepunkte auswählen.')



class HalteplanChoosePricesForm(FlaskForm):
    submit = SubmitField('Preise festlegen')
