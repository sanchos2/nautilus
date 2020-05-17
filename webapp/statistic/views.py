"""Statistic views."""
from datetime import date

import locale
import platform

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required


from webapp.statistic.forms import DateForm
from webapp.statistic.utils.query import query_sum_purchase, query_purchase_category, query_receipt_subcategory

blueprint = Blueprint('statistic', __name__, url_prefix='/statistics')


@blueprint.route('/my-outlay')  # noqa: WPS210
@login_required
def my_outlay():  # noqa: WPS210
    """Render page with statistics with my outlay."""
    title = 'Мои расходы'
    if platform.system() == 'Windows':
        locale.setlocale(locale.LC_ALL, 'russian')
    else:
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    form = DateForm()
    start_date = date.today().replace(day=1)
    end_date = date.today()
    text_date = date.today().strftime('%B %Y')
    query_sum = query_sum_purchase(current_user, start_date, end_date)
    query_purchase = query_purchase_category(current_user, start_date, end_date)
    query_receipt = query_receipt_subcategory(current_user, start_date, end_date)
    return render_template(
        'statistic/my_outlay.html',
        form=form,
        page_title=title,
        query_purchase=query_sum,
        query_category=query_purchase,
        query_subcategory=query_receipt,
        text_date=text_date,
    )


@blueprint.route('/process-outlay', methods=['POST'])  # noqa: WPS210
def process_outlay():  # noqa: WPS210
    """Date selection process."""
    title = 'Мои расходы'
    form = DateForm()
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        if start_date > end_date:
            flash('Дата начала не может быть больше даты конца периода')
            return redirect(url_for('statistic.my_outlay'))
        query_sum = query_sum_purchase(current_user, start_date, end_date)
        query_purchase = query_purchase_category(current_user, start_date, end_date)
        query_receipt = query_receipt_subcategory(current_user, start_date, end_date)
        flash('Данные обновлены')
        return render_template(
            'statistic/my_outlay.html',
            form=form,
            page_title=title,
            query_purchase=query_sum,
            query_category=query_purchase,
            query_subcategory=query_receipt,
            text_date='выбранный период'
        )
    for field, errors in form.errors.items():
        for error in errors:
            flash(
                f'Ошибка в поле "{getattr(form, field).label.text}": - {error}'
            )
    return redirect(url_for('statistic.my_outlay'))
