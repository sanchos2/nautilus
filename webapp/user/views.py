from flask import Blueprint, render_template, redirect, flash, url_for
from flask_login import current_user, logout_user, login_user, login_required

from webapp.user.forms import LoginForm
from webapp.user.models import User

blueprint = Blueprint('user', __name__, url_prefix='/users')


@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('receipt.my_receipt'))
    title = 'Авторизация'
    login_form = LoginForm()
    return render_template('user/login.html', page_title=title, form=login_form)


@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Вы вошли на сайт')
            return redirect(url_for('receipt.my_receipt'))
    flash('Неправильное имя пользователя или пароль')
    return redirect(url_for('user.login'))


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы успешно разлогинились')
    return redirect(url_for('index'))


@blueprint.route('/profile')
@login_required
def profile():
    title = 'Страница профиля пользователя'
    dev_message = 'Сделать форму профиля пользователя'
    return render_template('user/profile.html', page_title=title, dev_message=dev_message)


@blueprint.route('/recovery')
def recovery():
    title = 'Страница восстановления пароля'
    dev_message = 'Сделать форму восстановления пароля'
    return render_template('user/recovery.html', page_title=title, dev_message=dev_message)


@blueprint.route('/register')
def register():
    title = 'Страница регистрации пользователя'
    dev_message = 'Сделать форму регистрации пользователя'
    return render_template('user/register.html', page_title=title, dev_message=dev_message)