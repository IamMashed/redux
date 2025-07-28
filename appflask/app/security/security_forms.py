from flask_security.forms import LoginForm

from wtforms import PasswordField, BooleanField, SubmitField, StringField

from wtforms.validators import DataRequired


class ExtendedLoginForm(LoginForm):
    email = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')
