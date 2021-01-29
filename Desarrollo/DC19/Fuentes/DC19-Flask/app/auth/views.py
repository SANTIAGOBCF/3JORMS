from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import User
from ..email import send_email
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, \
    PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm
from requests import request as req


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid alias or password.')
    # print(url_for('auth.login'))
    # return render_template('auth/login.html', form=form)
    return render_template(url_for('auth.login') + '.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Usted ha sido desconectado.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        url = "https://dniruc.apisperu.com/api/v1/dni/" + form.dni.data + "?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InlpaHNpY0BnbWFpbC5jb20ifQ.JtcQWJs0oWX1bFMoxtfIDwooMXcbqeRBKTJADq7-p5Y"
        answer = req('GET', url).json()
        full_name_dni = answer.get('nombres') + " " + answer.get("apellidoPaterno") + " " + answer.get('apellidoMaterno')
        cui_dni = answer.get('codVerifica')
        if not cui_dni.isnumeric(): # cui no fue encontrado por la API
            cui_dni = int(form.cui.data)
        if form.full_name.data.lower() == full_name_dni.lower() and int(form.cui.data) == int(cui_dni):
            user = User(email=form.email.data,
                        alias=form.alias.data,
                        password=form.password.data,
                        dni = form.dni.data,
                        full_name = form.full_name.data,
                        cui = form.cui.data)
            db.session.add(user)
            db.session.commit()
            token = user.generate_confirmation_token()
            send_email(user.email, 'Confirma Tu Cuenta',
                       'auth/email/confirm', user=user, token=token)
            flash('Se le ha enviado un correo electrónico de confirmación por correo electrónico.')
            return redirect(url_for('auth.login'))
        else:
            flash('El nombre no coincide con el DNI-CUI.')
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('Ha confirmado su cuenta. ¡Gracias!')
    else:
        flash('El enlace de confirmación no es válido o ha caducado.')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirma Tu Cuenta',
               'auth/email/confirm', user=current_user, token=token)
    flash('Se le ha enviado un nuevo correo electrónico de confirmación por correo electrónico.')
    return redirect(url_for('main.index'))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Tu contraseña ha sido actualizada.')
            return redirect(url_for('main.index'))
        else:
            flash('Contraseña invalida.')
    return render_template("auth/change_password.html", form=form)


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Restablecer Su Contraseña',
                       'auth/email/reset_password',
                       user=user, token=token)
        flash('Se le ha enviado un correo electrónico con instrucciones para restablecer su contraseña.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('Tu contraseña ha sido actualizada.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data.lower()
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, 'Confirme su dirección de correo electrónico',
                       'auth/email/change_email',
                       user=current_user, token=token)
            flash('Se le ha enviado un correo electrónico con instrucciones para '
                    'confirmar que su nueva dirección de correo electrónico.')
            return redirect(url_for('main.index'))
        else:
            flash('Correo electrónico o contraseña no válidos.')
    return render_template("auth/change_email.html", form=form)


@auth.route('/change_email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash('Su dirección de correo electrónico se ha actualizado.')
    else:
        flash('Solicitud no válida.')
    return redirect(url_for('main.index'))
