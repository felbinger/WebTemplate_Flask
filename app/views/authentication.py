import requests
from flask import Blueprint, redirect, render_template, request, flash, url_for, session
from .utils import require_login, require_logout

authentication = Blueprint(__name__, 'authentication')


@authentication.route('/login', methods=['GET', 'POST'])
@require_logout
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            token = requests.post(
                f'{request.scheme}://{request.host}{url_for("auth_api")}',
                json={
                    'username': username,
                    'password': password
                }
            ).json().get('token')
            if token:
                # The next line can be removed, its useful for debugging.
                print(f'User {username} logged in with token: {token}')
                session['Access-Token'] = token
                return redirect(url_for('app.views.main.index'))
            else:
                flash('Credentials incorrect', 'danger')
        else:
            flash('Missing credentials', 'danger')
    return render_template('login.html')


@authentication.route('/logout', methods=['GET'])
@require_login
def logout():
    requests.delete(
        f'{request.scheme}://{request.host}{url_for("auth_api")}',
        headers={'Access-Token': session.get('Access-Token')},
    )
    session['Access-Token'] = None
    return redirect(url_for('app.views.main.index'), code=302)
