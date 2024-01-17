from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, FileField, SelectField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed

class PostForm(FlaskForm):
    title = StringField('Назва', validators=[DataRequired(), Length(min=2, max=100)])
    text = StringField('Текст', validators=[DataRequired()])
    image = FileField('Фото', validators=[FileAllowed(['jpg', 'png'])])
    enabled = BooleanField('Enabled', default=True)
    category = SelectField('Категорія', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Підтвердити')


class CategoryForm(FlaskForm):
    name = StringField('Назва', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Підтвердити')
