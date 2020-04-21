from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, HiddenField
from wtforms.validators import DataRequired


# костыль для валидации формы с SelectField
class NonValidatingSelectField(SelectField):
    def pre_validate(self, form):
        pass


class PurchaseForm(FlaskForm):
    date = DateField('Дата покупки', default=datetime.now(), render_kw={'class': 'form-control'})
    purchase = StringField('Наименование покупки', validators=[DataRequired()], render_kw={'class': 'form-control'})
    quantity = StringField('Количество', default=1, render_kw={'class': 'form-control'})
    sum = StringField('Сумма покупки', validators=[DataRequired()], render_kw={'class': 'form-control'})
    submit = SubmitField('Отправить', render_kw={'class': 'btn btn-primary'})


class AddCategoryForm(FlaskForm):
    receipt_id = StringField('ID позиции чека', validators=[DataRequired()])
    category = NonValidatingSelectField('Категория', choices=[], render_kw={'class': 'form-control'})
    submit = SubmitField('Отправить', render_kw={'class': 'btn btn-primary'})