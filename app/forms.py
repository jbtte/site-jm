from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField, DateField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User
from datetime import datetime

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    is_parent = BooleanField('Parent')
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class ParentInput(FlaskForm):
    ammount = DecimalField("Valor", validators=[DataRequired()])
    operation = RadioField(choices=[("1","depósito"), ("0", "retirada")], validators=[DataRequired()])
    description = StringField('Descrição')
    timestamp = DateField("Data", format='%d-%m-%Y', default=datetime.utcnow)
    submit = SubmitField('Confirmar')
