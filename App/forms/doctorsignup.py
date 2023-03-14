from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, StringField, PasswordField, IntegerField, validators
from wtforms.validators import InputRequired #Length
#from wtforms.widgets import html5 as h5widgets

class DoctorSignUp(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    npi = StringField('NPI number', validators = [InputRequired()])
    password = PasswordField('New Password', validators=[InputRequired()])
    submit = SubmitField('Sign Up', render_kw={'class': 'btn amber darken-4 waves-effect waves-blue'})
