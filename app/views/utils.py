from functools import wraps
from flask import session, redirect, url_for, request, flash
import requests


def require_login(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if session.get('Access-Token'):
            return view_func(*args, **kwargs)
        else:
            return redirect(url_for('app.views.authentication.login')), 403
    return wrapper


def require_logout(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if session.get('Access-Token'):
            # check if token is still valid
            resp = requests.get(
                f'{request.scheme}://{request.host}{url_for("auth_api")}',
                headers={'Access-Token': session.get('Access-Token')}
            )
            if resp.status_code != 401:
                return redirect(url_for('app.views.main.index')), 403
        return view_func(*args, **kwargs)
    return wrapper


def require_admin(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        user = requests.get(
            f'{request.scheme}://{request.host}{url_for("auth_api")}',
            headers={'Access-Token': session.get('Access-Token')}
        ).json().get('data')
        if user.get('role').get('name') == 'admin':
            return view_func(*args, **kwargs)
        else:
            flash('You\'re not allowed to request this resource')
            return redirect(url_for('app.views.main.index')), 403
    return wrapper
