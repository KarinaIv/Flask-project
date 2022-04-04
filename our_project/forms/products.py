from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms import FloatField
from wtforms.validators import DataRequired


class ProductsForm(FlaskForm):
    title = StringField('Название товара', validators=[DataRequired()])
    content = TextAreaField("Описание товара")
    price = FloatField('Цена товара', validators=[DataRequired()])
    # photo = ?
    submit = SubmitField('Применить')