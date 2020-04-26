"""Admin forms."""
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired


class NonValidatingSelectField(SelectField):
    """костыль для валидации формы с SelectField."""

    def pre_validate(self, form):
        """Override method."""
        pass  # noqa: WPS420


class CategoryForm(FlaskForm):
    """Form for adding product categories."""

    category = StringField(
        'Категория',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'},
    )
    submit = SubmitField('Отправить', render_kw={'class': 'btn btn-primary'})


class SubcategoryForm(FlaskForm):
    """Form for adding product subcategory."""

    category = NonValidatingSelectField(
        'Категория',
        choices=[],
        render_kw={'class': 'form-control'},
    )
    subcategory = StringField(
        'Cубкатегория',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'},
    )
    submit = SubmitField('Отправить', render_kw={'class': 'btn btn-primary'})
