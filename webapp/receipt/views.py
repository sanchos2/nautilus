from flask import Blueprint, render_template

from webapp.receipt.forms import ReceiptForm

blueprint = Blueprint('receipt', __name__, template_folder='receipt/')


@blueprint.route('/receipt')
def receipt():
    title = 'Мои чеки'
    receipt_form = ReceiptForm()
    return render_template('receipt/receipt.html', page_title=title, form=receipt_form)