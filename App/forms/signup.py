from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, StringField, PasswordField, validators
from wtforms.validators import InputRequired, Email

class SignUp(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('New Password', validators=[InputRequired()])
    submit = SubmitField('Sign Up', render_kw={'class': 'btn amber darken-4 waves-effect waves-blue'})