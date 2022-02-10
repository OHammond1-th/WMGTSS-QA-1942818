from flask import Blueprint, request, redirect, url_for, render_template, flash
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


@views.route('/Questions', methods=['GET', 'POST'])
@login_required
def question_list():
    courses = current_user.get_classes()

    if request.method == 'GET':
        elevated = current_user.is_elevated()
        course_ids = [course.ident for course in courses]
        questions_public = Question.get_public_questions(course_ids)
        questions_private = Question.get_private_questions(current_user.get_id())

        print(questions_public, questions_private)

        return render_template("question_list.html",
                               elevated=elevated,
                               courses=courses,
                               public_questions=questions_public,
                               private_questions=questions_private
                               )

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        course_input = request.form['selected-course']
        publishable = True if request.form.get('publishable') == "on" else False

        for course in courses:
            if course_input.strip() == course.name:
                course_input = course.ident

        if title and description and course_input and publishable is not None and current_user.hasnt_interacted_today():
            question_id = str(Question.create_question(course_input, current_user.ident, title, description, publishable))
            current_user.update_interaction()
            return redirect(url_for('views.question_page', question_id=question_id))

        flash("Submission failed due to missing field")
        return redirect(url_for("views.question_list"))

    else:
        return "<h1>405: Method not allowed.</h1>"


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


@views.route("/Questions/<int:question_id>/Comment/New")
def create_comment(question_id, parent=None):
    if parent:
        comment_text = request.form[f'{parent}-comment']
    else:
        comment_text = request.form[f'new-comment']

    if comment_text:
        success = Comment.create_comment(question_id, current_user.ident, comment_text, parent)

        if success:
            return redirect(url_for("views.question_page", question_id=question_id))

        else:
            return error_html()

    else:
        return redirect(url_for("views.question_page", question_id=question_id))


@views.route("/Deleting/<int:question_id>")
@login_required
def delete_question(question_id):
    success = Question.delete(question_id)

    if success:
        return redirect(url_for("views.question_list"))

    else:
        return error_html()


@views.route("/Answering/<int:question_id>", methods=['POST'])
@login_required
def answer_question(question_id):
    success = Question.provide_answer(question_id, request.form[f'{question_id}-answer'])

    if success:
        return redirect(url_for("views.question_page", question_id=question_id))

    else:
        return error_html()


def error_html():
    return "<h1>An error occurred whilst processing the last request." \
           "Please go back on your browser to return to site<h1>"
