from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Length
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from .models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=10)], render_kw={"class": "form-control"})
    remember = BooleanField('Remember Me', render_kw={"class": "form-check-input"})
    submit = SubmitField('Login', render_kw={"class": "btn btn-primary"})

class TaskForm(FlaskForm):
    title = StringField('Назва завдання')
    submit = SubmitField('Додати завдання')

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=14), 
                # Regexp('^[A-Za-a][A-Za-z0-9_.]*$', 0, 'Username must only have letters, numbers, dots or underscores')       
                                        ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField("Sign up")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')
    
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already registered')

class LoginForm2(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Login")