from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_required, login_user, logout_user, current_user
from .models import Course, User, Question, Comment
from werkzeug.security import check_password_hash, generate_password_hash

auth = Blueprint('auth', __name__)


@auth.route('/Login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.get_by_username(username)

        if user:
            if user.password is None:
                user_id = user.ident
                return redirect(url_for("auth.pass_set", user_id=user_id))

            correct_password = check_password_hash(user.password, password)

            if correct_password:

                login_user(user)
                return redirect(request.args.get('next') or url_for("views.home"))

        return render_template("login.html", failed=True)

    else:
        return "<h1>405: Method not allowed.</h1>"


@auth.route('/SetPass', methods=['GET', 'POST'])
def pass_set():
    if request.method == 'GET':
        return render_template("pass_set.html")

    if request.method == 'POST':
        new_pass = request.form['password']
        User.set_password_by_id(request.args.get('user_id'), generate_password_hash(new_pass))
        return redirect(url_for("auth.login"))

    else:
        return "<h1>405: Method not allowed.</h1>"
