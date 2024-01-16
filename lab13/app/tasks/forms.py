from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class TaskForm(FlaskForm):
    title = StringField('Назва завдання')
    submit = SubmitField('Додати завдання')