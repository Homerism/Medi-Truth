from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField
from wtforms.validators import InputRequired


class QueryForm(FlaskForm):
    textarea = StringField(
        'Text', render_kw={"rows": 100, "cols": 100}, validators=[InputRequired()])
    submit = SubmitField('Submit', render_kw={
                         'class': 'btn amber darken-4 waves-effect waves-light'})
