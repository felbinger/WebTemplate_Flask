import requests
from flask import Blueprint, render_template, request, flash, url_for, session
from .utils import require_login, require_admin

main = Blueprint(__name__, 'main')


@main.route('/', methods=['GET'])
def index():
    user = requests.get(
        f'{request.scheme}://{request.host}{url_for("auth_api")}',
        headers={'Access-Token': session.get('Access-Token')}
    ).json().get('data') or None

    return render_template('index.html', user=user), 200


@main.route('/settings', methods=['GET', 'POST'])
@require_login
def settings():
    header = {'Access-Token': session.get('Access-Token')}
    if request.method == 'POST':
        if request.form is not None:
            action = request.form.get('action')

            if action == 'updatePassword':
                if len(request.form.get('password1')) >= 8:
                    if request.form.get('password1') == request.form.get('password2'):
                        resp = requests.put(
                            f'{request.scheme}://{request.host}{url_for("user_api")}/me',
                            headers=header,
                            json={
                                'password': request.form.get('password1')
                            }
                        )
                        if resp.status_code != 200:
                            flash(f'Unable to update password: {resp.json().get("message")}', 'danger')
                        else:
                            flash('Password has been updated!', 'success')
                    else:
                        flash('The entered Password\'s are not the same!', 'danger')
                else:
                    flash('The password is too short (>= 8 characters)', 'danger')

            elif action == 'update':

                resp = requests.put(
                    f'{request.scheme}://{request.host}{url_for("user_api")}/me',
                    headers=header,
                    json={
                        'displayName': request.form.get('displayName'),
                        'email': request.form.get('email'),
                        'status': request.form.get('status')
                    }
                )
                if resp.status_code != 200:
                    flash(f'Unable to update your account: {resp.json().get("message")}', 'danger')
                else:
                    flash('Your account has been updated!', 'success')

    user = requests.get(
        f'{request.scheme}://{request.host}{url_for("auth_api")}',
        headers={'Access-Token': session.get('Access-Token')}
    ).json().get('data')

    return render_template('settings.html', user=user), 200


@main.route('/dashboard', methods=['GET', 'POST'])
@require_login
@require_admin
def dashboard():
    header = {'Access-Token': session.get('Access-Token')}
    if request.method == 'POST':
        if request.form is not None:
            action = request.form.get('action')

            if action == 'createAccount':

                username = request.form.get('username')
                password = request.form.get('password')
                email = request.form.get('email')
                role = request.form.get('role')

                if not username:
                    flash('Unable to create account: Username cannot be emtpy!', 'danger')
                else:
                    if not password:
                        flash('Unable to create account: Password cannot be emtpy!', 'danger')
                    else:
                        if len(password) < 8:
                            flash('Password is too short!', 'danger')
                        else:
                            if not email:
                                flash('Unable to create account: E-Mail cannot be emtpy!', 'danger')
                            else:
                                if not role:
                                    flash('Unable to create account: Role cannot be emtpy!', 'danger')
                                else:
                                    resp = requests.post(
                                        f'{request.scheme}://{request.host}{url_for("user_api")}',
                                        headers=header,
                                        json={
                                            'username': username,
                                            'password': password,
                                            'email': email,
                                            'role': role
                                        }
                                    )
                                    if resp.status_code != 201:
                                        flash(f'Unable to create account: {resp.json().get("message")}', 'danger')
                                    else:
                                        flash('Account has been created successfully!', 'success')

            elif action == 'updateAccount':
                public_id = request.form.get('id')
                if public_id:
                    resp = requests.put(
                        f'{request.scheme}://{request.host}{url_for("user_api")}/{public_id}',
                        json={
                            'username': request.form.get('username'),
                            'displayName': request.form.get('displayName'),
                            'email': request.form.get('email'),
                            'role': request.form.get('role')
                        },
                        headers=header
                    )
                    if resp.status_code != 200:
                        flash(f'Unable to update account: {resp.json().get("message")}', 'danger')
                    else:
                        flash('Account has been update!', 'success')
                else:
                    flash('You need to provide an uuid to update an account!', 'danger')

            elif action == 'deleteAccount':
                public_id = request.form.get('id')
                if public_id:
                    resp = requests.delete(
                        f'{request.scheme}://{request.host}{url_for("user_api")}/{public_id}',
                        headers=header
                    )
                    if resp.status_code != 204:
                        flash(f'Unable to delete account: {resp.json().get("message")}', 'danger')
                    else:
                        flash('Account has been deleted!', 'success')
                else:
                    flash('You need to provide an uuid to delete an account!', 'danger')

            elif action == 'updatePassword':
                public_id = request.form.get('id')
                if public_id:
                    if request.form.get('password1') == request.form.get('password2'):
                        if request.form.get('password2') != "":
                            resp = requests.put(
                                f'{request.scheme}://{request.host}{url_for("user_api")}/{public_id}',
                                headers=header,
                                json={
                                    'password': request.form.get('password1')
                                }
                            )
                            if resp.status_code != 200:
                                flash(f'Unable to update password: {resp.json().get("message")}', 'danger')
                            else:
                                flash('Password has been updated!', 'success')
                        else:
                            flash('You are not allowed to set an emtpy password!', 'danger')
                    else:
                        flash('The entered Password\'s are not the same!', 'danger')
                else:
                    flash('You need to provide an uuid to change the password of an account!', 'danger')

            elif action == 'createRole':
                name = request.form.get('name')
                description = request.form.get('description')
                if not name or not description:
                    flash('Unable to create Role: Name and description cannot be emtpy!', 'danger')
                else:
                    resp = requests.post(
                        f'{request.scheme}://{request.host}{url_for("role_api")}',
                        headers=header,
                        json={
                            'name': name,
                            'description': description
                        }
                    )
                    if resp.status_code != 201:
                        flash(f'Unable to create role: {resp.json().get("message")}', 'danger')
                    else:
                        flash('Role has been created successfully!', 'success')

            elif action == 'updateRole':
                name = request.form.get('name')
                description = request.form.get('description')
                if not name:
                    flash('Unable to update Role: Name cannot be emtpy!', 'danger')
                else:
                    if not description:
                        flash('Unable to update Role: Description cannot be emtpy!', 'danger')
                    else:
                        resp = requests.put(
                            f'{request.scheme}://{request.host}{url_for("role_api")}/{name}',
                            headers=header,
                            json={
                                'description': description
                            }
                        )
                        if resp.status_code != 200:
                            flash(f'Unable to update role: {resp.json().get("message")}', 'danger')
                        else:
                            flash('Role has been created successfully!', 'success')

            elif action == 'deleteRole':
                name = request.form.get('name')
                if name:
                    resp = requests.delete(
                        f'{request.scheme}://{request.host}{url_for("role_api")}/{name}',
                        headers=header
                    )
                    if resp.status_code != 204:
                        flash(f'Unable to delete role: {resp.json().get("message")}', 'danger')
                    else:
                        flash('Role has been deleted!', 'success')
                else:
                    flash('You need to provide an name to delete a role!', 'danger')

    data = dict()
    data['accounts'] = requests.get(
        f'{request.scheme}://{request.host}{url_for("user_api")}',
        headers={'Access-Token': session.get('Access-Token')}
    ).json().get('data')

    data['roles'] = requests.get(
        f'{request.scheme}://{request.host}{url_for("role_api")}',
        headers={'Access-Token': session.get('Access-Token')}
    ).json().get('data')

    return render_template('dashboard.html', data=data), 200
