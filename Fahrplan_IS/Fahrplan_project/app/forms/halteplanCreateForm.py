
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, Length
from wtforms.fields.choices import SelectMultipleField

class HalteplanCreateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    streckenName = SelectField('Strecken Name', choices=[], validators=[DataRequired()])
    submit = SubmitField('Create Halteplan')
    haltepunkte = SelectMultipleField('Haltepunkte', choices=["Wien","Budapest", "Sofia"])  # TODO get from strecken system
