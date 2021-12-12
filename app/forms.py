from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class ConsumeForm(FlaskForm):
    choices = [('coke', 'Coke'), ('celsius', 'Celsius Energy Drink'),
               ('candy', 'Candy')]
    thing = SelectMultipleField(u'Thing you eat next', choices=choices)
    submit = SubmitField('Eat IT!')
