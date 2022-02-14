from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_required, login_user, logout_user, current_user
from .models import Course, User, Question, Comment
from werkzeug.security import check_password_hash, generate_password_hash

# Blueprint variable to be referenced by our app
auth = Blueprint('auth', __name__)


@auth.route('/Login', methods=['GET', 'POST'])
def login():
    """
    Login window to handle user session creation
    :return: The login window
    """

    # if the user has arrived on this page render its html
    if request.method == 'GET':
        return render_template("login.html")

    # if the user has submitted a form attempt a login
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # get the user from the database
        user = User.get_by_username(username)

        # if the user exists check the given password
        if user:

            # if the user doesnt have a password take them to the create password screen
            if user.password is None:
                user_id = user.ident
                return redirect(url_for("auth.pass_set", user_id=user_id))

            # Get confirmation of if this is the correct password
            correct_password = check_password_hash(user.password, password)

            # if it is correct login the user session and return the destination of the users original request or the
            # home page
            if correct_password:

                login_user(user)
                return redirect(request.args.get('next') or url_for("views.home"))

        # if the login fails render login html again but with failure text displayed
        return render_template("login.html", failed=True)

    else:
        return "<h1>405: Method not allowed.</h1>"


@auth.route('/SetPass', methods=['GET', 'POST'])
def pass_set():
    """
    Allows the user to change their password
    :return: The destination html
    """
    # if the user has arrived on this page render the html
    if request.method == 'GET':
        return render_template("pass_set.html")

    # if the user has submitted a form use the given value to generate a password
    if request.method == 'POST':
        new_pass = request.form['password']

        # Sets the password with a hashed version of the value
        User.set_password_by_id(request.args.get('user_id'), generate_password_hash(new_pass))
        return redirect(url_for("auth.login"))

    else:
        return "<h1>405: Method not allowed.</h1>"
