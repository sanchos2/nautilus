from flask import Blueprint, render_template
from flask_login import login_required, current_user

from webapp.receipt.temp_data import receipt_set, receipt_set_detailed
from webapp.receipt.forms import ReceiptForm, PurchaseForm
from webapp.receipt.models import Purchase, Receipt

blueprint = Blueprint('receipt', __name__, url_prefix='/receipt')


@blueprint.route('/')
@login_required
def receipt():
    title = 'Проверка чека'
    receipt_form = ReceiptForm()
    return render_template('receipt/receipt.html', page_title=title, form=receipt_form)


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
    my_det_receipt = Receipt.query.filter(Receipt.purchase_id == purchase).all()
    return render_template('receipt/my_detailed_receipt.html', page_title=title, receipt=my_det_receipt)


@blueprint.route('/my-outlay')
@login_required
def my_outlay():
    title = 'Мои расходы'
    return render_template('receipt/my_outlay.html', page_title=title)


@blueprint.route('/qrscaner')
@login_required
def qrscaner():
    title = 'Сканер'
    return render_template('receipt/qrscaner.html', page_title=title)




