from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from webapp.user.models import User


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={'class': 'form-control'})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={'class': 'form-control'})
    remember_me = BooleanField('Запомнить меня', default=False, render_kw={'class': 'form-check-input'})
    submit = SubmitField('Войти', render_kw={'class': 'btn btn-primary'})


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={'class': 'form-control'})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'class': 'form-control'})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={'class': 'form-control'})
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')],
                              render_kw={'class': 'form-control'})
    submit = SubmitField('Зарегистрироваться', render_kw={'class': 'btn btn-primary'})

    def validate_username(self, username):
        users_count = User.query.filter_by(username=username.data).count()
        if users_count > 0:
            raise ValidationError('Пользователь с таким именем уже существует')

    def validate_email(self, email):
        email_count = User.query.filter_by(email=email.data).count()
        if email_count > 0:
            raise ValidationError('Пользователь с таким email уже зарегистрирован')


class ProfileForm(FlaskForm):
    fns_login = StringField('Ведите номер телефона в формате +7ХХХХХХХХХХ',
                            validators=[DataRequired(), Length(min=12, max=12)], render_kw={'class': 'form-control'})
    fns_password = PasswordField('Пароль полученный в sms сообщении от KKT-NALOG', render_kw={'class': 'form-control'})
    submit = SubmitField('Обновить профиль', validators=[DataRequired()], render_kw={'class': 'btn btn-primary'})

    def validate_fns_login(self, fns_login):
        fns_login_count = User.query.filter_by(fns_login=fns_login.data).count()
        if fns_login_count > 0:
            raise ValidationError('Пользователь с таким номером телефона уже зарегистрирован')


class RegisterFnsForm(FlaskForm):
    telephone = StringField('Ведите номер телефона в формате +7ХХХХХХХХХХ',
                            validators=[DataRequired(), Length(min=12, max=12)], render_kw={'class': 'form-control'})
    submit = SubmitField('Запросить пароль', validators=[DataRequired()], render_kw={'class': 'btn btn-primary'})

    def validate_telephone(self, fns_login):
        fns_login_count = User.query.filter_by(fns_login=fns_login.data).count()
        if fns_login_count > 0:
            raise ValidationError('Пользователь с таким номером телефона уже зарегистрирован')


class RecoveryFnsForm(FlaskForm):
    telephone = StringField('Ведите номер телефона в формате +7ХХХХХХХХХХ',
                            validators=[DataRequired(), Length(min=12, max=12)], render_kw={'class': 'form-control'})
    submit = SubmitField('Запросить пароль', validators=[DataRequired()], render_kw={'class': 'btn btn-primary'})
