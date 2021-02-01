from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, PostForm
from .. import db
from ..models import User, Role, Post, Permission
from ..decorators import admin_required
from .. import socketio
from flask_socketio import send

@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        post = Post(body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))
    #  posts = Post.query.order_by(Post.timestamp.desc()).all()
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['DC19_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('index.html', form=form, posts=posts,
                           pagination=pagination)


@main.route('/user/<alias>')
def user(alias):
    user = User.query.filter_by(alias=alias).first_or_404()
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        #current_user.alias = form.alias
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user', alias=current_user.alias))
    #form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.alias = form.alias.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        #user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('The profile has been updated.')
        return redirect(url_for('.user', alias=user.alias))
    form.email.data = user.email
    form.alias.data = user.alias
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    #form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)

@main.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    return render_template('main-chat.html')


@main.route('/group_chat', methods=['GET', 'POST'])
@login_required
def group_chat():
    return render_template('group-chat.html')

@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    send(msg, broadcast = True)

@main.route('/foro', methods=['GET', 'POST'])
@login_required
def foro():
    return render_template('foro.html')

@main.route('/topic', methods=['GET', 'POST'])
@login_required
def topic():
    return render_template('topic.html')