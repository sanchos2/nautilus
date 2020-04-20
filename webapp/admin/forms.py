from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired

from webapp import db
from webapp.receipt.models import Category

# костыль для валидации формы с SelectField
class NonValidatingSelectField(SelectField):
    def pre_validate(self, form):
        pass


class CategoryForm(FlaskForm):
    category = StringField('Категория', validators=[DataRequired()], render_kw={'class': 'form-control'})
    submit = SubmitField('Отправить', render_kw={'class': 'btn btn-primary'})


class SubcategoryForm(FlaskForm):
    category = NonValidatingSelectField('Категория', choices=[], render_kw={'class': 'form-control'})
    subcategory = StringField('Cубкатегория', validators=[DataRequired()], render_kw={'class': 'form-control'})
    submit = SubmitField('Отправить', render_kw={'class': 'btn btn-primary'})



