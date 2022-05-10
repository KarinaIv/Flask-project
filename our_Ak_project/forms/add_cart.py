from flask_wtf import FlaskForm
from wtforms.fields import IntegerField
from wtforms.validators import DataRequired
from wtforms import SubmitField


class AddCart(FlaskForm):
    cnt = IntegerField('Количество товара', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
