from flask import Blueprint, render_template, flash, url_for, redirect
from flask_login import current_user

from webapp.receipt.my_data import auth_login, auth_password
from webapp.receipt.find_receipt import qr_parser, check_receipt, get_receipt
from webapp.receipt.forms import ReceiptForm

blueprint = Blueprint('receipt', __name__, template_folder='receipt/')


@blueprint.route('/receipt')
def receipt():
    if not current_user.is_authenticated:
        return redirect(url_for('user.login'))
    else:
        title = 'Проверка чека'
        receipt_form = ReceiptForm()
        return render_template('receipt/receipt.html', page_title=title, form=receipt_form)


@blueprint.route('/process-qrparser', methods=['POST'])
def process_qrparser():
    form = ReceiptForm()
    if form.validate_on_submit():
        qr_text = form.qrtext.data
        data_from_qr = qr_parser(qr_text)
        data_from_receipt_valid = check_receipt(data_from_qr)
        if data_from_receipt_valid:
            flash('Мы нашли Ваш чек')
            try:
                flash('Пробуем получить полные данные по Вашему чеку')
                data_from_receipt = get_receipt(data_from_qr, auth_login, auth_password)
                kwargs1 = {'data_from_qr': data_from_qr, 'data_from_receipt_valid': data_from_receipt_valid,
                          'data_from_receipt': data_from_receipt['document']['receipt']['items']}
                return render_template('receipt/qrdata.html', **kwargs1)
            except KeyError:
                flash('Полные данные по чеку не получены')
                kwargs2 = {'data_from_qr': data_from_qr, 'data_from_receipt_valid': data_from_receipt_valid}
                return render_template('receipt/qrdata.html', **kwargs2)
        else:
            flash('Что то пошло не так :( Мы попробуем проверить Ваш чек позднее')
            flash(data_from_receipt_valid)
            return redirect(url_for('receipt.receipt'))


@blueprint.route('/my-receipt')
def my_receipt():
    title = 'Мои чеки'
    return render_template('receipt/my_receipt.html', page_title=title)


@blueprint.route('/my-outlay')
def my_outlay():
    title = 'Мои расходы'
    return render_template('receipt/my_outlay.html', page_title=title)
