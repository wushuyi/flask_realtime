from flask.ext.wtf import Form
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(Form):
    """Accepts a nickname and a room."""
    name = StringField('name', validators=[DataRequired()])
    room = StringField('room', validators=[DataRequired()])
    submit = SubmitField('Enter Chatroom')
