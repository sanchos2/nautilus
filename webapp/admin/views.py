from flask import Blueprint
from webapp.user.decorators import admin_required

blueprint = Blueprint('admin', __name__, template_folder='')


@blueprint.route('/admin')
@admin_required
def admin_index():
    return 'Привет админ'