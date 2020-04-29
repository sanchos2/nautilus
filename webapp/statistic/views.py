"""Statistic views."""
from datetime import datetime

from flask import Blueprint, render_template
from flask_login import current_user, login_required
from sqlalchemy import func

from webapp.db import db
from webapp.receipt.models import Category, Purchase, PurchaseCategory

blueprint = Blueprint('statistic', __name__, url_prefix='/statistics')


@blueprint.route('/my-outlay')
@login_required
def my_outlay():
    """Render page with statistics with my outlay."""
    title = 'Мои расходы'
    # Отчет № 1 Сумма покупок за месяц(период) по пользователю
    # select sum(purchase.sum) from purchase
    # where date between '2020-04-10' and now();
    start_date = '2020-02-10'
    end_date = datetime.now()
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

    return render_template(
        'statistic/my_outlay.html',
        page_title=title,
        query_purchase=query_sum_purchase,
        query_category=query_purchase_category,
    )
