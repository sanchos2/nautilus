from flask import Blueprint, jsonify, request, redirect, flash, render_template, url_for, make_response
from flask_login import current_user, login_required

from webapp.db import db
from webapp.user.models import User
from webapp.receipt.my_data import auth_login, auth_password
from webapp.receipt.find_receipt import qr_parser, check_receipt, get_receipt, format_date
from webapp.receipt.forms import ReceiptForm
from webapp.receipt.models import Receipt, Purchase

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')


# данный маршрут в прод не идет
@blueprint.route('/process-qrparser', methods=['POST'])
@login_required
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


@blueprint.route('/qrscaner-process', methods=['POST'])
@login_required
def qrscaner_process():
    qr_text = request.data.decode('utf-8')
    data_from_qr = qr_parser(qr_text)
    # fn_number - fn, fd_number - i, fpd_number - fp
    try:
        if Purchase.query.filter_by(fn_number=data_from_qr['fn']).first():
            raise ValueError('fn_number in Table!!!')
        else:
            new_purchase = Purchase(user_id=current_user.id, fn_number=data_from_qr['fn'],
                                    fd_number=data_from_qr['i'], fpd_number=data_from_qr['fp'],
                                    receipt_type=data_from_qr['n'], sum=data_from_qr['s'],
                                    date=format_date(data_from_qr['t']))
            db.session.add(new_purchase)
            db.session.commit()
    except ValueError:
        print('fn_number уже есть в таблице! Чек не добавляем.')
        flash('Этот чек Вы уже добавляли!')
    return make_response(jsonify(data_from_qr), 200)
