from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash
from .models import Course, User, Question, Comment

views = Blueprint('views', __name__)


@views.route('/Login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.get_by_username(username)

        if user:

            correct_password = check_password_hash(user.password, password)

            if correct_password:

                login_user(user)
                return redirect(request.args.get('next') or url_for("views.question_list"))

        return render_template("login.html", failed=True)

    else:
        return "<h1>405: Method not allowed.</h1>"


@views.route('/')
def home():
    return redirect(url_for('views.login'))


@views.route('/Logout')
@login_required
def logout():

    logout_user()

    return redirect(url_for('views.login'))


@views.route('/Questions')
@login_required
def question_list():
    questions_public = Question.get_public_questions(current_user.get_classes())
    questions_private = Question.get_private_questions(current_user.get_id())

    return render_template("question_list.html",
                           public_questions=questions_public,
                           private_questions=questions_private
                           )


@views.route('/Questions/<int:question_id>')
@login_required
def question_page(question_id):

    question = Question.get_question_by_id(question_id)
    course = Course.get_by_id(question.course)
    author = User.get_by_id(question.author)
    comments = Comment.get_post_comments(question_id)

    if question:
        return render_template("question_page.html", question=question, author=author, comments=comments, course=course)
    else:
        return redirect(url_for("views.question_list"))
