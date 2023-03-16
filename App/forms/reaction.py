from flask_wtf import FlaskForm
from wtforms import SelectMultipleField
from wtforms.validators import InputRequired

class DoctorReaction(FlaskForm):
    reaction = SelectMultipleField('Do You Approve or Disapprove of this article', coerce=str, choices=[('Approve','Disapprove')])
