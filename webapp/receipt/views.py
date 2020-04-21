from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user

from webapp import db
from webapp.receipt.forms import PurchaseForm, AddCategoryForm
from webapp.receipt.models import Category, Purchase, Receipt

blueprint = Blueprint('receipt', __name__, url_prefix='/receipt')


@blueprint.route('/my-receipt')
@login_required
def my_receipt():
    title = 'Мои покупки'
    form = PurchaseForm()
    my_purchase = Purchase.query.filter(Purchase.user_id == current_user.id).all()
    return render_template('receipt/my_receipt.html', page_title=title, purchase=my_purchase, form=form)


@blueprint.route('/my-detailed-receipt/<purchase>')
@login_required
def my_detailed_receipt(purchase):
    title = 'Мой чек'
    form = AddCategoryForm()
    category_choices = Category.query.all()
    form.category.choices = [(items.id, items.category) for items in category_choices]
    my_det_receipt = Receipt.query.filter(Receipt.purchase_id == purchase).all()
    return render_template('receipt/my_detailed_receipt.html', page_title=title,
                           receipt=my_det_receipt, form=form)


@blueprint.route('/qrscaner')
@login_required
def qrscaner():
    title = 'Сканер'
    return render_template('receipt/qrscaner.html', page_title=title)


@blueprint.route('/commit-category-to-receipt', methods=['POST'])
@login_required
def commit_category_to_receipt():
    form = AddCategoryForm()
    if form.validate_on_submit():
        receipt = Receipt.query.get(form.receipt_id.data)
        receipt.category = form.category.data
        db.session.add(receipt)
        db.session.commit()
        flash('Категория добавлена')
        return redirect(request.referrer)
    else:
        flash('Категория НЕ добавлена')
        return redirect(request.referrer)

