from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email

class SignUp(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email', validators=[Email(), InputRequired()])
    password = PasswordField('New Password', validators=[InputRequired()])
    submit = SubmitField('Sign Up', render_kw={'class': 'btn amber darken-4 waves-effect waves-blue'})


class LogIn(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('New Password', validators=[InputRequired()])
    submit = SubmitField('Login', render_kw={'class': 'btn amber darken-4 waves-effect waves-light'})
