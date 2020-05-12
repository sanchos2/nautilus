"""Statistic forms."""
from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField
from wtforms.validators import DataRequired


class DateForm(FlaskForm):
    """Choice date for statistic."""

    start_date = DateField(
        'Введите дату начала периода',
        validators=[DataRequired('Введите дату')],
        format='%Y-%m-%d',  # noqa: WPS323
        render_kw={'class': 'form-control', 'type': 'date'},
    )
    end_date = DateField(
        'Введите дату конца периода',
        validators=[DataRequired()],
        format='%Y-%m-%d',  # noqa: WPS323
        render_kw={'class': 'form-control', 'type': 'date'},
    )
    submit = SubmitField(
        'Обновить',
        validators=[DataRequired()],
        render_kw={'class': 'btn btn-primary'},
    )
