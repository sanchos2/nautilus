"""Receipt views."""
from flask import Blueprint, flash, redirect, render_template, request
from flask_login import current_user, login_required

from webapp.db import db
from webapp.receipt.models import Category, Purchase, Receipt
from webapp.receipt.forms import AddCategoryForm, PurchaseForm

blueprint = Blueprint('receipt', __name__, url_prefix='/receipt')


@blueprint.route('/my-receipt')
@login_required
def my_receipt():
    """Render my receipt page."""
    title = 'Мои покупки'
    form = PurchaseForm()
    my_purchase = Purchase.query.filter(
        Purchase.user_id == current_user.id
    ).all()
    return render_template(
        'receipt/my_receipt.html',
        page_title=title,
        purchase=my_purchase,
        form=form,
    )


@blueprint.route('/my-detailed-receipt/<purchase>')
@login_required
def my_detailed_receipt(purchase):
    """Render detailed receipt page."""
    title = 'Мой чек'
    form = AddCategoryForm()
    category_choices = Category.query.all()
    form.category.choices = [
        (category.id, category.category) for category in category_choices
    ]
    my_det_receipt = Receipt.query.filter(
        Receipt.purchase_id == purchase
    ).all()
    return render_template(
        'receipt/my_detailed_receipt.html',
        page_title=title,
        receipt=my_det_receipt,
        form=form,
    )


@blueprint.route('/qrscaner')
@login_required
def qrscaner():
    """Render template with QR scanner."""
    title = 'Сканер'
    return render_template(
        'receipt/qrscaner.html',
        page_title=title,
    )


@blueprint.route('/commit-category-to-receipt', methods=['POST'])
@login_required
def commit_category_to_receipt():
    """Add a category to the receipt and write to a database."""
    form = AddCategoryForm()
    if form.validate_on_submit():
        receipt = Receipt.query.get(form.receipt_id.data)
        receipt.category = form.category.data
        db.session.add(receipt)
        db.session.commit()
        flash('Категория добавлена')
        return redirect(request.referrer)
    flash('Категория НЕ добавлена')
    return redirect(request.referrer)
