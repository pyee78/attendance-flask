import secrets
import os
from PIL import Image
from flask import render_template, flash, redirect, url_for, request
from attendance import app
from attendance.forms import RegistrationForm, LoginForm, UpdateAccountForm
from attendance import bcrypt, db
from attendance.models import User
from flask_login import login_user, current_user, logout_user, login_required


# HOME route
@app.route("/")
@app.route("/home")
def home():  # probably doesn't matter what I call this function
    return render_template("home.html", title="HOME")


# REGISTER route
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # hash the password they created in the form
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # initialize the user, using the hashed password, not what they entered
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)

        # database commands to insert the user object and commit changes
        db.session.add(user)
        db.session.commit()

        # flash success message
        flash(f'Account created for {form.username.data}!', 'success')

        # redirect to login screen
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


# LOGIN route
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Unsuccessful. Please check email address & password', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


def save_picture(form_pic):
    random_hex = secrets.token_hex(8)
    # _ is a placeholder for a variable I know I'm not going to use
    _, f_ext = os.path.splitext(form_pic.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_filename)
    output_size =  (125, 125)

    # Pillow methods to resize the orignail picture
    i = Image.open(form_pic)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_filename


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                          image_file = image_file, form=form)
