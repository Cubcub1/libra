from datetime import datetime

from flask import session, current_app, redirect, url_for, render_template, abort, flash
from flask_login import current_user, login_required

from ..lib.qiniu_util import upload_qiniu
from ..decorators import admin_required
from ..email import send_email
from ..models import User, Role
from .forms import NameForm, EditProfileForm, EditProfileAdminForm
from .. import db
from . import main


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if current_app.config['LIBRA_ADMIN']:
                send_email(current_app.config['LIBRA_ADMIN'], 'New User', 'mail/new_user', user=user)
        else:
            session['konwn'] = True
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False),
                           current_time=datetime.utcnow())


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        avatar_data = form.avatar.data
        file_name = upload_qiniu(avatar_data.read())
        current_user.avatar_url = file_name
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('你的信息已经更新了.')
        return redirect(url_for('.user', username=current_user.username))
    form.avatar.data = current_user.avatar_url
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user)
    if form.validate_on_submit():
        avatar_data = form.avatar.data
        # import pdb;pdb.set_trace()
        file_name = upload_qiniu(avatar_data.read())
        user.avatar_url = file_name
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('你的信息已经更新了.')
        return redirect(url_for('.user', username=current_user.username))
    form.avatar.data = current_user.avatar_url
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)
