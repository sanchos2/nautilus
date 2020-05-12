"""Statistic views."""
from datetime import date

import locale
import platform

from flask import Blueprint, render_template
from flask_login import current_user, login_required
from sqlalchemy import func

from webapp.db import db
from webapp.receipt.models import Category, Purchase, PurchaseCategory, Subcategory, Receipt, ReceiptSubcategory

blueprint = Blueprint('statistic', __name__, url_prefix='/statistics')


@blueprint.route('/my-outlay')  # noqa: WPS210
@login_required
def my_outlay():
    """Render page with statistics with my outlay."""
    title = 'Мои расходы'
    if platform.system() == 'Windows':
        locale.setlocale(locale.LC_ALL, 'russian')
    else:
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    # Отчет № 1 Сумма покупок за месяц(период) по пользователю
    # select sum(purchase.sum) from purchase
    # where date between '2020-04-10' and now();
    start_date = date.today().replace(day=1)
    end_date = date.today()
    text_date = date.today().strftime('%B %Y')
    query_sum_purchase = db.session.query(  # noqa: WPS221
        func.sum(Purchase.sum)
    ).filter(
        Purchase.user_id == current_user.id
    ).filter(
        Purchase.date.between(start_date, end_date)
    ).scalar()
    # Отчет № 2 сумма покупок за месяц(период) по сумме покупкам и их категориям
    # select c.category, sum(p.sum) as sm
    # from purchase as p left outer join purchase_category as pc
    # on p.id = pc.purchase_id
    # left outer join category as c
    # on pc.category_id = c.id
    # where date between '2020-01-20' and now()
    # group by c.category
    # order by sm desc;

    query_purchase_category = db.session.query(  # noqa: WPS221
        Category.category, func.sum(Purchase.sum)
    ).join(
        PurchaseCategory, Purchase.id == PurchaseCategory.purchase_id, isouter=True
    ).join(
        Category, PurchaseCategory.category_id == Category.id, isouter=True
    ).filter(
        Purchase.date.between(start_date, end_date)
    ).filter(
        Purchase.user_id == current_user.id
    ).group_by(
        Category.category
    ).order_by(
        Category.category
    ).all()

    # отчет № 3 такой же как и №2 только по чекам и субкатегориям

    query_receipt_subcategory = db.session.query(  # noqa: WPS221
        Subcategory.subcategory, func.sum(Receipt.sum) / 100
    ).join(
        ReceiptSubcategory, Receipt.id == ReceiptSubcategory.receipt_id, isouter=True
    ).join(
        Subcategory, ReceiptSubcategory.subcategory_id == Subcategory.id, isouter=True
    ).join(
        Purchase, Receipt.purchase_id == Purchase.id
    ).filter(
        Purchase.date.between(start_date, end_date)
    ).filter(
        Purchase.user_id == current_user.id
    ).group_by(
        Subcategory.subcategory
    ).order_by(
        Subcategory.subcategory
    ).all()

    return render_template(
        'statistic/my_outlay.html',
        page_title=title,
        query_purchase=query_sum_purchase,
        query_category=query_purchase_category,
        query_subcategory=query_receipt_subcategory,
        text_date=text_date
    )
