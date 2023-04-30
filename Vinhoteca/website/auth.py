from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user

class Auth():
    
    auth = Blueprint('auth', __name__)

    @auth.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')

            user = User.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password, password):
                    flash('Login realizado com sucesso!', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.home'))
                else:
                    flash('Senha incorreta, tente novamente', category='error')
            else:
                flash('Email não cadastrado', category='error')

        return render_template("login.html", user=current_user)


    @auth.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('auth.login'))


    @auth.route('/sign-up', methods=['GET', 'POST'])
    def sign_up():
        if request.method == 'POST':
            email = request.form.get('email')
            first_name = request.form.get('firstName')
            password1 = request.form.get('password1')
            password2 = request.form.get('password2')
            
            user = User.query.filter_by(email=email).first()
            if user:
                flash('Email já cadastrado', category='error')
            elif len(email) < 7:
                flash('Email precisa ter mais do que 6 caracteres', category='error')
            elif len(first_name) < 2:
                flash('Primeiro nome deve ter mais do que 3 caracteres.', category='error')
            elif password1 != password2:
                flash('Senhas não coincidem', category='error')
            elif len(password1) < 7:
                flash('Senha deve ter no mínimo 7 caracteres.', category='error')
            else:
                new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                    password1, method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash('Conta criada!', category='success')
                return redirect(url_for('views.home'))

        return render_template("sign_up.html", user=current_user)
