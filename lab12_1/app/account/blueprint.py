from flask import render_template, redirect, url_for, flash, Blueprint
from extensions import db, bcrypt
import os
from datetime import datetime
import secrets
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, UpdateAccountForm
from .models import User
from flask_login import login_user, current_user, logout_user, login_required

bp = Blueprint('account', __name__, template_folder="templates/account")

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Account was created', category="success")
        return redirect(url_for("account.login"))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in {field}: {error}', category="danger")

    return render_template('register.html', form=form, title="Register")

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("resume.index"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You have been logged in!', category="success")
            return redirect(url_for("resume.index"))
        else:
            flash("Login unsuccessful", category='warning')

    return render_template('login2.html', form=form, title="Login")

@bp.route('/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    flash('Ви вийшли з системи', 'info')
    return redirect(url_for('account.login'))

@bp.route("/users", methods=['GET', 'POST'])
def users():
    all_users = User.query.all()
    return render_template('users.html', all_users=all_users)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(bp.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)
    return picture_fn

@bp.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    image_file = url_for(bp.root_path, filename='static/profile_pics/' + current_user.image_file)

    change_password_form = ChangePasswordForm()
    update_account_form = UpdateAccountForm()

    if update_account_form.validate_on_submit():
        if update_account_form.picture.data:
            picture_file = save_picture(update_account_form.picture.data)
            current_user.image_file = picture_file
        current_user.username = update_account_form.username.data
        current_user.email = update_account_form.email.data
        current_user.about_me = update_account_form.about_me.data
        db.session.commit()
        flash("Your account was updated", 'success')
        return redirect("account.account")
    
    if change_password_form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, change_password_form.old_password.data):
            current_user.password = bcrypt.generate_password_hash(change_password_form.new_password.data).decode('utf-8')
            db.session.commit()
            flash('Password changed successfully', 'success')
        else:
            flash('Old password is incorrect', 'danger')

    return render_template("account.html", title="Account", image_file=image_file, change_password_form=change_password_form, update_account_form=update_account_form)

@bp.after_request
def after_request(response):
    if current_user:
        current_user.last_seen = datetime.now()
        try:
            db.session.commit()
        except:
            flash('Error while update user last seen!', 'danger')
        return response  