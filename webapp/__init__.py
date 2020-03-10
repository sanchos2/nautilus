from flask import Flask

from webapp.model import db


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    return app


app = create_app()


@app.route("/")
def hello():
    return app.config['TEXT']
