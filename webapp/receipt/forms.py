from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired


class NonValidatingSelectField(SelectField):
    """костыль для валидации формы с SelectField"""
    def pre_validate(self, form):
        pass


class PurchaseForm(FlaskForm):
    """Purchase form"""
    date = DateField('Дата покупки', default=datetime.now(), render_kw={'class': 'form-control'})
    purchase = StringField('Наименование покупки', validators=[DataRequired()], render_kw={'class': 'form-control'})
    quantity = StringField('Количество', default=1, render_kw={'class': 'form-control'})
    sum = StringField('Сумма покупки', validators=[DataRequired()], render_kw={'class': 'form-control'})
    submit = SubmitField('Отправить', render_kw={'class': 'btn btn-primary'})


class AddCategoryForm(FlaskForm):
    """Add category to purchase"""
    receipt_id = StringField('ID позиции чека', validators=[DataRequired()])
    category = NonValidatingSelectField('Категория', choices=[], render_kw={'class': 'form-control'})
    submit = SubmitField('Отправить', render_kw={'class': 'btn btn-primary'})
