import yaml
import os

from flask import Flask, render_template

from webapp.model import db

basedir = os.path.abspath(os.path.dirname(__file__))
file_yaml = os.path.join(basedir, '..', 'config.yaml')

with open(file_yaml, 'r') as yml_file:
    yml_str = yml_file.read()
    data = yaml.safe_load(yml_str)


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(data['DEVELOPMENT'])
    db.init_app(app)
    return app


appl = create_app()


@appl.route("/")
def index():
    title = 'Nautilus'
    return render_template('index.html', page_title=title, name=appl.config['TEXT'])

@appl.route("/requests")
def requests():
    pass

#  run server
#  set FLASK_APP=webapp && set FLASK_ENV=development && set FLASK_DEBUG=1 && flask run