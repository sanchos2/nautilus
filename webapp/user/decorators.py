"""Decorator admin_required."""
from functools import wraps

from flask import current_app, flash, request, redirect, url_for
from flask_login import config, current_user


def admin_required(func):  # noqa: WPS212, WPS231
    """Admin required decorator."""
    @wraps(func)  # noqa: WPS430
    def decorated_view(*args, **kwargs):
        if request.method in config.EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif current_app.config.get('LOGIN DISABLED'):
            return func(*args, **kwargs)
        elif not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        elif not current_user.is_admin:
            flash('Эта страница доступна только админам')
            return redirect(url_for('index'))
        return func(*args, **kwargs)
    return decorated_view
