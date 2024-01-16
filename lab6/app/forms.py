from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=10)], render_kw={"class": "form-control"})
    remember = BooleanField('Remember Me', render_kw={"class": "form-check-input"})
    submit = SubmitField('Login', render_kw={"class": "btn btn-primary"})

class TaskForm(FlaskForm):
    title = StringField('Назва завдання')
    submit = SubmitField('Додати завдання')