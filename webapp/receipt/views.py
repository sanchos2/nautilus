"""Receipt views."""
from flask import Blueprint, flash, redirect, render_template, request
from flask_login import current_user, login_required

from webapp.db import db
from webapp.receipt.models import Category, Purchase, Receipt, PurchaseCategory, Subcategory, ReceiptSubcategory
from webapp.receipt.forms import AddCategoryForm, AddSubcategoryForm, PurchaseForm

blueprint = Blueprint('receipt', __name__, url_prefix='/receipt')


@blueprint.route('/my-receipt')
@login_required
def my_receipt():
    """Render my receipt page."""
    title = 'Мои покупки'
    form = PurchaseForm()
    form_category = AddCategoryForm()
    category_choices = Category.query.all()
    form_category.category.choices = [
        (category.id, category.category) for category in category_choices
    ]
    my_purchase = Purchase.query.filter(
        Purchase.user_id == current_user.id
    ).all()
    return render_template(
        'receipt/my_receipt.html',
        page_title=title,
        purchase=my_purchase,
        form=form,
        form_category=form_category,
    )


@blueprint.route('/my-detailed-receipt/<purchase>')
@login_required
def my_detailed_receipt(purchase):
    """Render detailed receipt page."""
    title = 'Мой чек'
    form = AddSubcategoryForm()
    subcategory_choices = Subcategory.query.all()
    form.subcategory.choices = [
        (subcategory.id, subcategory.subcategory) for subcategory in subcategory_choices
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


@blueprint.route('/commit-category-to-purchase', methods=['POST'])
@login_required
def commit_category_to_purchase():
    """Add a category to the purchase and write to a database."""
    form_category = AddCategoryForm()
    if form_category.validate_on_submit():
        purchase = Purchase.query.get(form_category.purchase_id.data)
        category = Category.query.get(form_category.category.data)
        change_category = PurchaseCategory.query.filter(PurchaseCategory.purchase_id == purchase.id).first()
        if change_category:
            change_category.purchase_id = purchase.id
            change_category.category_id = category.id
            db.session.commit()
            flash('Категория обновлена')
            return redirect(request.referrer)
        new_relation = PurchaseCategory(purchase_id=purchase.id, category_id=category.id)
        db.session.add(new_relation)
        db.session.commit()
        flash('Категория добавлена')
        return redirect(request.referrer)
    flash('Категория НЕ добавлена')
    return redirect(request.referrer)


@blueprint.route('/commit-subcategory-to-receipt', methods=['POST'])
@login_required
def commit_subcategory_to_receipt():
    """Add a subcategory to the receipt and write to a database."""
    form_subcategory = AddSubcategoryForm()
    if form_subcategory.validate_on_submit():
        receipt = Receipt.query.get(form_subcategory.receipt_id.data)
        subcategory = Subcategory.query.get(form_subcategory.subcategory.data)
        change_subcategory = ReceiptSubcategory.query.filter(ReceiptSubcategory.receipt_id == receipt.id).first()
        if change_subcategory:
            change_subcategory.receipt_id = receipt.id
            change_subcategory.subcategory_id = subcategory.id
            db.session.commit()
            flash('Субкатегория обновлена')
            return redirect(request.referrer)
        new_relation = ReceiptSubcategory(receipt_id=receipt.id, subcategory_id=subcategory.id)
        db.session.add(new_relation)
        db.session.commit()
        flash('Субкатегория добавлена')
        return redirect(request.referrer)
    flash('Субкатегория НЕ добавлена')
    return redirect(request.referrer)
