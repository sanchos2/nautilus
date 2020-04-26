"""Landing views."""
from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user

blueprint = Blueprint('landing', __name__)


@blueprint.route('/')
def index():
    """Render root page."""
    if current_user.is_authenticated:
        return redirect(url_for('receipt.my_receipt'))
    title = 'Сервис контроля за личными расходами'
    return render_template('index.html', page_title=title)
