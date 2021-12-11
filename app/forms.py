from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember_me = BooleanField('Remember Me')
  submit = SubmitField('Sign In')

class ConsumeForm(FlaskForm):
  thing = SelectMultipleField(u'Thing', 
    choices=[('cpp', 'C++'), 
    ('py', 'Python'), 
    ('text', 'Plain Text')])
  submit = SubmitField('Eat IT!')



 