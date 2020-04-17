from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired


class ReceiptForm(FlaskForm):
    qrtext = StringField('Введите QR код', validators=[DataRequired()], render_kw={'class': 'form-control'})
    submit = SubmitField('Отправить', render_kw={'class': 'btn btn-primary'})


class PurchaseForm(FlaskForm):
    date = DateField('Дата покупки', default=datetime.now(), render_kw={'class': 'form-control'})
    purchase = StringField('Наименование покупки', validators=[DataRequired()], render_kw={'class': 'form-control'})
    quantity = StringField('Количество', default=1, render_kw={'class': 'form-control'})
    sum = StringField('Сумма покупки', validators=[DataRequired()], render_kw={'class': 'form-control'})
    submit = SubmitField('Отправить', render_kw={'class': 'btn btn-primary'})