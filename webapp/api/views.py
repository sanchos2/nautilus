from flask import Blueprint, jsonify, request, redirect, flash, render_template, url_for, make_response
from flask_login import current_user, login_required

from webapp.db import db
from webapp.receipt.find_receipt import qr_parser, check_receipt, get_receipt, format_date
from webapp.receipt.forms import ReceiptForm, PurchaseForm
from webapp.receipt.models import Receipt, Purchase

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')


# данный маршрут в прод не идет
@blueprint.route('/process-qrparser', methods=['POST'])
@login_required
def process_qrparser():
    form = ReceiptForm()
    auth_login = current_user.fns_login
    auth_password = current_user.fns_password
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
        if Purchase.query.filter_by(fd_number=data_from_qr['i']).first(): # TODO сделать проверку по трем параметрам чека
            raise ValueError('fd_number in Table!!!')
        else:
            new_purchase = Purchase(user_id=current_user.id, fn_number=data_from_qr['fn'],
                                    fd_number=data_from_qr['i'], fpd_number=data_from_qr['fp'],
                                    receipt_type=data_from_qr['n'], sum=data_from_qr['s'],
                                    date=format_date(data_from_qr['t']))
            db.session.add(new_purchase)
            db.session.commit()
    except ValueError:
        print('fd_number уже есть в таблице! Чек не добавляем.')
        flash('Этот чек Вы уже добавляли!')
    return make_response(jsonify(data_from_qr), 200)


@blueprint.route('/process-manual-add-purchase', methods=['POST'])
@login_required
def process_manual_add_purchase():
    form = PurchaseForm()
    if form.validate_on_submit():
        sum = form.sum.data.replace(',', '.')
        quantity = form.quantity.data.replace(',', '.')
        new_purchase = Purchase(user_id=current_user.id,
                                receipt_type=1,
                                sum=sum,
                                date=form.date.data,
                                organization='Вручную',
                                loaded='fetched',
                                )
        db.session.add(new_purchase)
        db.session.commit()
        new_receipt = Receipt(purchase_id=new_purchase.id,
                              product=form.purchase.data,
                              price=float(sum) * 100 / float(quantity),
                              quantity=quantity,
                              sum=float(sum) * 100)
        db.session.add(new_receipt)
        db.session.commit()
        flash('Покупка успешно добавлена')
        return redirect(url_for('receipt.my_receipt'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Ошибка в поле "{getattr(form, field).label.text}": - {error}')
        return redirect(url_for('receipt.my_receipt'))