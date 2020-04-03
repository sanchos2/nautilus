from flask import Blueprint, render_template, redirect, flash, url_for
from flask_login import current_user, logout_user, login_user, login_required

from webapp import db
from webapp.user.forms import LoginForm, RegistrationForm
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


@blueprint.route('/profile/')
@login_required
def profile():
    title = 'Страница профиля пользователя'
    user = current_user
    return render_template('user/profile.html', page_title=title, dev_message=user)


@blueprint.route('/recovery')
def recovery():
    title = 'Страница восстановления пароля'
    dev_message = 'Сделать форму восстановления пароля'
    return render_template('user/recovery.html', page_title=title, dev_message=dev_message)


@blueprint.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('receipt.my_receipt'))
    title = 'Регистрация нового пользователя'
    register_form = RegistrationForm()
    return render_template('user/register.html', page_title=title, form=register_form)


@blueprint.route('/process-register', methods=['POST'])
def process_register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, telephone=form.telephone.data, role='user')
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались')
        return redirect(url_for('user.login'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Ошибка в поле "{getattr(form, field).label.text}": - {error}')
        return redirect(url_for('user.register'))
