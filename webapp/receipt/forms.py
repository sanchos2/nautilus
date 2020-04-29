"""Receipt forms."""
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired


class NonValidatingSelectField(SelectField):
    """костыль для валидации формы с SelectField."""

    def pre_validate(self, form):
        """Override method."""
        pass  # noqa: WPS420


class PurchaseForm(FlaskForm):
    """Purchase form."""

    date = DateField(
        'Дата покупки',
        default=datetime.now(),
        render_kw={'class': 'form-control'},
    )
    purchase = StringField(
        'Наименование покупки',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'},
    )
    quantity = StringField(
        'Количество',
        default=1,
        render_kw={'class': 'form-control'},
    )
    sum = StringField(  # noqa: WPS125
        'Сумма покупки',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'},
    )
    submit = SubmitField('Отправить', render_kw={'class': 'btn btn-primary'})


class AddCategoryForm(FlaskForm):
    """Add category to purchase."""

    purchase_id = StringField('ID позиции чека', validators=[DataRequired()])
    category = NonValidatingSelectField(
        'Категория',
        choices=[],
        render_kw={'class': 'form-control'},
    )
    submit = SubmitField('Отправить', render_kw={'class': 'btn btn-primary'})


class AddSubcategoryForm(FlaskForm):
    """Add subcategory to receipt."""

    receipt_id = StringField('ID позиции чека', validators=[DataRequired()])
    subcategory = NonValidatingSelectField(
        'Субкатегория',
        choices=[],
        render_kw={'class': 'form-control'},
    )
    submit = SubmitField('Отправить', render_kw={'class': 'btn btn-primary'})
