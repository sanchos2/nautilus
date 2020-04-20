from flask import Blueprint, jsonify, request, redirect, flash, render_template, url_for, make_response
from flask_login import current_user, login_required

from webapp.db import db
from webapp.receipt.find_receipt import qr_parser, check_receipt, get_receipt, format_date
from webapp.receipt.forms import PurchaseForm
from webapp.receipt.models import Receipt, Purchase

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')


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