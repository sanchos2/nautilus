from flask import Blueprint, render_template
from flask_login import login_required

from webapp.receipt.temp_data import receipt_set, receipt_set_detailed
from webapp.receipt.forms import ReceiptForm

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
    title = 'Мои чеки'
    return render_template('receipt/my_receipt.html', page_title=title, receipt_dict=receipt_set)


@blueprint.route('/my-detailed-receipt')
@login_required
def my_detailed_receipt():
    title = 'Мой чек'
    return render_template('receipt/my_detailed_receipt.html', page_title=title, receipt_dict_detailed=receipt_set_detailed)


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




