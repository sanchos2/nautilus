"""SQLAlchemy query."""
from sqlalchemy import func

from webapp.db import db
from webapp.receipt.models import Category, Purchase, PurchaseCategory, Subcategory, Receipt, ReceiptSubcategory


def query_sum_purchase(current_user, start_date, end_date):
    """Query from database.
    Отчет № 1 Сумма покупок за месяц(период) по пользователю
    select sum(purchase.sum) from purchase
    """
    return db.session.query(  # noqa: WPS221
        func.sum(Purchase.sum)
    ).filter(
        Purchase.user_id == current_user.id
    ).filter(
        Purchase.date.between(start_date, end_date)
    ).scalar()


def query_purchase_category(current_user, start_date, end_date):
    """Query from database.
    Отчет № 2 сумма покупок за месяц(период) по сумме покупкам и их категориям
    select c.category, sum(p.sum) as sm
    from purchase as p left outer join purchase_category as pc
    on p.id = pc.purchase_id
    left outer join category as c
    on pc.category_id = c.id
    where date between '2020-01-20' and now()
    group by c.category
    order by sm desc;
    """
    return db.session.query(  # noqa: WPS221
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


def query_receipt_subcategory(current_user, start_date, end_date):
    """Query from database.
    отчет № 3 такой же как и №2 только по чекам и субкатегориям
    """
    return db.session.query(  # noqa: WPS221
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
