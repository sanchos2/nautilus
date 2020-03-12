import yaml
import os

from flask import Flask, flash, render_template, redirect, url_for
from flask_login import LoginManager, current_user, login_user, logout_user

from webapp.models import db, User
from webapp.forms import LoginForm, ReceiptForm
from webapp.decorators import admin_required

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
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app


app = create_app()


@app.route('/')
def index():
    title = 'Nautilus'
    return render_template('index.html', page_title=title, name=app.config['TEXT'])


@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    title = 'Авторизация'
    login_form = LoginForm()
    return render_template('user/login.html', page_title=title, form=login_form)


@app.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Вы вошли на сайт')
            return redirect(url_for('receipt'))
    flash('Неправильное имя пользователя или пароль')
    return redirect(url_for('login'))


@app.route('/admin')
@admin_required
def admin_index():
    return 'Привет админ'


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/receipt')
def receipt():
    title = 'Мои чеки'
    receipt_form = ReceiptForm()
    return render_template('receipt/receipt.html', page_title=title, form=receipt_form)

#  run server
#  set FLASK_APP=webapp && set FLASK_ENV=development && set FLASK_DEBUG=1 && flask run
