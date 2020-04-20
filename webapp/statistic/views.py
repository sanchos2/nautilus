from flask import Blueprint, render_template
from flask_login import login_required


blueprint = Blueprint('statistic', __name__, url_prefix='/statistics')


@blueprint.route('/my-outlay')
@login_required
def my_outlay():
    title = 'Мои расходы'

    return render_template('statistic/my_outlay.html', page_title=title)