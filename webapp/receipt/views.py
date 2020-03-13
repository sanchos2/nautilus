from flask import Blueprint, render_template, flash

from webapp.receipt.my_data import auth_login, auth_password
from webapp.receipt.find_receipt import qr_parser, check_receipt, get_receipt
from webapp.receipt.forms import ReceiptForm

blueprint = Blueprint('receipt', __name__, template_folder='receipt/')


@blueprint.route('/receipt')
def receipt():
    title = 'Мои чеки'
    receipt_form = ReceiptForm()
    return render_template('receipt/receipt.html', page_title=title, form=receipt_form)


@blueprint.route('/process-qrparser', methods=['POST'])
def process_qrparser():
    form = ReceiptForm()
    if form.validate_on_submit():
        qr_text = form.qrtext.data
        data_from_qr = qr_parser(qr_text)
        data_from_receipt_valid = check_receipt(data_from_qr)
        data_from_receipt = get_receipt(data_from_qr, auth_login, auth_password )
    return render_template('receipt/qrdata.html', data_from_qr=data_from_qr,
                           data_from_receipt_valid=data_from_receipt_valid,
                           data_from_receipt=data_from_receipt['document']['receipt']['items'])