import yaml
import os

from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, current_user

from webapp.user.models import db, User
from webapp.admin.views import blueprint as admin_blueprint
from webapp.api.views import blueprint as api_blueprint
from webapp.receipt.views import blueprint as receipt_blueprint
from webapp.user.views import blueprint as user_blueprint

basedir = os.path.abspath(os.path.dirname(__file__))
file_yaml = os.path.join(basedir, '..', 'config.yaml')

with open(file_yaml, 'r') as yml_file:
    yml_str = yml_file.read()
    data = yaml.safe_load(yml_str)


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(data['DEVELOPMENT'])
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'
    app.register_blueprint(api_blueprint)
    app.register_blueprint(receipt_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(admin_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    return app


app = create_app()


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('receipt.my_receipt'))
    title = 'Nautilus'
    return render_template('index.html', page_title=title, name='Сервис контроля за личными расходами')


#  run server
#  set FLASK_APP=webapp && set FLASK_ENV=development && set FLASK_DEBUG=1 && flask run --host 192.168.0.39 --cert=adhoc
