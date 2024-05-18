
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.choices import SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length


class HalteplanEditForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    streckenName = SelectField('Strecken Name', choices=[], validators=[DataRequired()])
    haltepunkte = SelectMultipleField('Haltepunkte',choices=[])  # TODO get from strecken system
    submit = SubmitField('Speichern')