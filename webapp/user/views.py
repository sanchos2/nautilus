from flask import Blueprint, flash, render_template, redirect,  url_for
from flask_login import current_user, login_required, login_user, logout_user

from webapp import db
from webapp.receipt.utils.receipt_handler import recovery_pass, registration_fns
from webapp.user.forms import LoginForm, ProfileForm, RecoveryFnsForm, RegistrationForm,  RegisterFnsForm
from webapp.user.models import User

blueprint = Blueprint('user', __name__, url_prefix='/users')


@blueprint.route('/login', endpoint='login')
def login():
    """Login required"""
    if current_user.is_authenticated:
        return redirect(url_for('receipt.my_receipt'))
    title = 'Авторизация'
    login_form = LoginForm()
    return render_template('user/login.html', page_title=title, form=login_form)


@blueprint.route('/process-login', methods=['POST'])
def process_login():
    """Authorization process"""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            if user.fns_login and user.fns_password:
                flash('Вы вошли на сайт')
                return redirect(url_for('receipt.my_receipt'))
            else:
                flash('Для работы с сервисом Вам необходимо заполнить следующие данные:')
                return redirect(url_for('user.profile', username=current_user.username))
    flash('Неправильное имя пользователя или пароль')
    return redirect(url_for('user.login'))


@blueprint.route('/logout')
@login_required
def logout():
    """Logout process"""
    logout_user()
    flash('Вы успешно разлогинились')
    return redirect(url_for('landing.index'))


@blueprint.route('/profile/<username>')
@login_required
def profile(username):
    """Render user profile page"""
    title = 'Страница профиля пользователя'
    user = User.query.filter_by(username=username).first_or_404()
    profile_form = ProfileForm()
    register_fns_form = RegisterFnsForm()
    recovery_fns_form = RecoveryFnsForm()
    return render_template('user/profile.html', page_title=title, form=profile_form,
                           form_fns=register_fns_form, form_recovery=recovery_fns_form, user=user)


@blueprint.route('/process-profile', methods=['POST'])
@login_required
def process_profile():
    """Update user profile process"""
    form = ProfileForm()
    if form.validate_on_submit():
        username = current_user.username
        user = User.query.filter_by(username=username).first_or_404()
        if form.fns_login.data:
            user.fns_login = form.fns_login.data
        if form.fns_password.data:
            user.fns_password = form.fns_password.data
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно обновили свой профиль')
        return redirect(url_for('receipt.my_receipt'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в поле "{}": - {}'.format(getattr(form, field).label.text, error))
        return redirect(url_for('user.profile', username=current_user.username))


@blueprint.route('/recovery')
def recovery():
    """Recovery password page"""
    title = 'Страница восстановления пароля'
    dev_message = 'Сделать форму восстановления пароля'
    return render_template('user/recovery.html', page_title=title, dev_message=dev_message)


@blueprint.route('/register')
def register():
    """User registration page"""
    if current_user.is_authenticated:
        return redirect(url_for('receipt.my_receipt'))
    title = 'Регистрация нового пользователя'
    register_form = RegistrationForm()
    return render_template('user/register.html', page_title=title, form=register_form)


@blueprint.route('/process-register', methods=['POST'])
def process_register():
    """User registration process"""
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, role='user')
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


@blueprint.route('/process-register-fns', methods=['POST'])
@login_required
def process_register_fns():
    """Registration in FNS process"""
    form = RegisterFnsForm()
    if form.validate_on_submit():
        email = current_user.email
        name = current_user.username
        phone = form.telephone.data
        registration_fns(email, name, phone)
        flash('Ждите SMS от KKT-NALOG')
        return redirect(url_for('user.profile', username=current_user.username))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Ошибка в поле "{getattr(form, field).label.text}": - {error}')
        return redirect(url_for('user.profile', username=current_user.username))


@blueprint.route('/process-recovery-fns', methods=['POST'])
@login_required
def process_recovery_fns():
    """Recovery password from FNS"""
    form = RecoveryFnsForm()
    if form.validate_on_submit():
        phone = form.telephone.data
        recovery_pass(phone)
        flash('Ждите SMS от KKT-NALOG')
        return redirect(url_for('user.profile', username=current_user.username))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Ошибка в поле "{getattr(form, field).label.text}": - {error}')
        return redirect(url_for('user.profile', username=current_user.username))
