"""Main file."""
import os

import yaml


from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate

from webapp.db import db
from webapp.user.models import User
from webapp.admin.views import blueprint as admin_blueprint
from webapp.api.views import blueprint as api_blueprint
from webapp.landing.views import blueprint as landing_blueprint
from webapp.receipt.views import blueprint as receipt_blueprint
from webapp.statistic.views import blueprint as statistic_blueprint
from webapp.user.views import blueprint as user_blueprint

basedir = os.path.abspath(os.path.dirname(__file__))
file_yaml = os.path.join(basedir, '..', 'config.yaml')

with open(file_yaml, 'r') as yml_file:
    yml_str = yml_file.read()
    config_data = yaml.safe_load(yml_str)


def create_app():  # noqa: WPS213
    """Create Flask APP."""
    app = Flask(__name__)
    app.config.from_mapping(config_data['PRODUCTION'])
    db.init_app(app)
    migrate = Migrate(app, db)  # noqa: F841
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'
    app.register_blueprint(api_blueprint)
    app.register_blueprint(landing_blueprint)
    app.register_blueprint(receipt_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(statistic_blueprint)

    @login_manager.user_loader  # noqa: WPS430
    def load_user(user_id):  # noqa: WPS430
        """Get user id."""
        return User.query.get(user_id)
    return app
