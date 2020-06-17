"""API views."""
from flask import Blueprint, flash, jsonify
from flask import make_response, request, redirect, url_for
from flask_login import current_user, login_required

from webapp.db import db
from webapp.receipt.models import Purchase, Receipt
from webapp.receipt.forms import PurchaseForm
from webapp.receipt.utils.receipt_handler import format_date, qr_parser

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')


@blueprint.route('/qrscaner-process', methods=['POST'])
@login_required
def qrscaner_process():
    """Add data from QR code to database."""
    qr_text = request.data.decode('utf-8')
    data_from_qr = qr_parser(qr_text)
    # fn_number - fn, fd_number - i, fpd_number - fp
    try:
        if Purchase.query.filter(  # noqa: WPS337
            Purchase.fd_number == data_from_qr['i'],
            Purchase.fn_number == data_from_qr['fn'],
            Purchase.fpd_number == data_from_qr['fp'],
        ).first():
            # чека
            raise ValueError('Purchase already in database!')
        else:
            new_purchase = Purchase(
                user_id=current_user.id,
                fn_number=data_from_qr['fn'],
                fd_number=data_from_qr['i'],
                fpd_number=data_from_qr['fp'],
                receipt_type=data_from_qr['n'],
                sum=data_from_qr['s'],
                date=format_date(data_from_qr['t']),
            )
            db.session.add(new_purchase)
            db.session.commit()
            flash('Покупка добавлена, содержимое появится в течении 2х минут')
    except ValueError:
        print('Покупка уже таблице! Чек не добавляем.')
        flash('Этот чек Вы уже добавляли!')
    return make_response(jsonify(data_from_qr), 200)


@blueprint.route('/process-manual-add-purchase', methods=['POST'])  # noqa: WPS210
@login_required
def process_manual_add_purchase():  # noqa: WPS210
    """Manually add purchase to database."""
    form = PurchaseForm()
    if form.validate_on_submit():
        sum = form.sum.data.replace(',', '.')  # noqa: WPS125
        quantity = form.quantity.data.replace(',', '.')
        new_purchase = Purchase(
            user_id=current_user.id,
            receipt_type=1,
            sum=sum,
            date=form.date.data,
            organization='Вручную',
            loaded='fetched',
        )
        db.session.add(new_purchase)
        db.session.commit()
        new_receipt = Receipt(
            purchase_id=new_purchase.id,
            product=form.purchase.data,
            price=float(sum) * 100 / float(quantity),
            quantity=quantity,
            sum=float(sum) * 100,
        )
        db.session.add(new_receipt)
        db.session.commit()
        flash('Покупка успешно добавлена')
        return redirect(url_for('receipt.my_receipt'))
    for field, errors in form.errors.items():
        for error in errors:
            flash(
                f'Ошибка в поле "{getattr(form, field).label.text}": - {error}'
            )
    return redirect(url_for('receipt.my_receipt'))
