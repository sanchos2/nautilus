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
    telephone = DecimalField('Ведите номер телефона в формате +71001232121',
                             validators=[DataRequired(), Length(min=12, max=12)], render_kw={'class': 'form-control'})
    submit = SubmitField('Зарегистрироваться', render_kw={'class': 'btn btn-primary'})

    def validate_username(self, username):
        users_count = User.query.filter_by(username=username.data).count()
        if users_count > 0:
            raise ValidationError('Пользователь с таким именем уже существует')

    def validate_email(self, email):
        email_count = User.query.filter_by(email=email.data).count()
        if email_count > 0:
            raise ValidationError('Пользователь с таким email уже зарегистрирован')

    def validate_telephone(self, telephone):
        telephone_count = User.query.filter_by(telephone=telephone.data).count()
        if telephone_count > 0:
            raise ValidationError('Пользователь с таким номером телефона уже зарегистрирован')

