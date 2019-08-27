from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user

from .forms import LoginForm
from . import auth
from ..models import User


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(url_for('main.index'))
        flash('无效的用户名或密码.')
    return render_template('auth/login.html', form=form)
