import traceback

from flask import Blueprint, request, redirect, url_for, render_template, flash, escape
from flask_login import login_required, logout_user, current_user
from .models import Course, User, Question, Comment

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return redirect(url_for('views.question_list'))


@views.route('/Logout')
@login_required
def logout():

    logout_user()

    return redirect(url_for('views.home'))


@views.route('/Questions', methods=['GET', 'POST'])
@login_required
def question_list():
    try:
        courses = current_user.get_classes()

        if request.method == 'GET':
            elevated = current_user.is_elevated()
            course_ids = [course.ident for course in courses]

            try:
                questions_public = Question.get_public_questions(course_ids)
                questions_private = Question.get_private_questions(current_user.get_id())
            except TypeError:
                questions_public = []
                questions_private = []

            print(questions_public, questions_private)

            return render_template("question_list.html",
                                   elevated=elevated,
                                   courses=courses,
                                   public_questions=questions_public,
                                   private_questions=questions_private
                                   )

        if request.method == 'POST':
            title = escape(request.form['title'])
            description = escape(request.form['description'])
            course_input = escape(request.form['selected-course'])
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

    except EOFError as e:
        print(e)
        return "<h2>You are not enrolled or an error has occurred. " \
               "Please contact the system administrator if there is a problem <h2>"


@views.route('/Questions/<int:question_id>', methods=['GET', 'POST'])
@login_required
def question_page(question_id):

    if request.method == 'GET':
        question = Question.get_question_by_id(question_id)
        course = Course.get_by_id(question.course)
        author = User.get_by_id(question.author)
        user = current_user
        comments = Comment.get_post_comments(question_id)

        print(comments)

        if question:
            return render_template("question_page.html", question=question,
                                   author=author, user=user, comments=comments, course=course)
        else:
            return redirect(url_for("views.question_list"))

    if request.method == 'POST':
        parent = escape(request.form['comment-parent'])
        text = escape(request.form['comment-text'])

        if int(parent) == -1:
            parent = "NULL"

        if text:
            success = Comment.create_comment(question_id, current_user.ident, text, parent)

            if not success:
                return error_html()

        return redirect(url_for("views.question_page", question_id=question_id))

    else:
        return "<h1>405: Method not allowed.</h1>"


@views.route("/Questions/<int:question_id>/Deleting")
@login_required
def delete_question(question_id):
    success = Question.delete(question_id)

    if success:
        return redirect(url_for("views.question_list"))

    else:
        return error_html()


@views.route("/Questions/<int:question_id>/Comments/<int:comment_id>/Deleting")
@login_required
def delete_comment(question_id, comment_id):
    Comment.soft_delete_comment(comment_id)
    return redirect(url_for("views.question_page", question_id=question_id))


@views.route("/Questions/<int:question_id>/Answer", methods=['GET', 'POST'])
@login_required
def answer_question(question_id):

    if current_user.is_elevated() and request.method == 'GET':
        return render_template("question_answer.html", question=Question.get_question_by_id(question_id))

    if current_user.is_elevated() and request.method == 'POST':
        answer = escape(request.form['answer'])

        # Default for empty answer is None so it must be converted from string to NoneType
        answer = answer if answer is not "None" else None
        Question.provide_answer(question_id, answer)

    return redirect(url_for("views.question_page", question_id=question_id))


@views.route("/Questions/<int:question_id>/Publish")
@login_required
def publish_question(question_id):
    success = Question.publish(question_id)

    if success:
        return redirect(url_for("views.question_list"))

    else:
        return error_html()


@views.route("/Question/<int:question_id>/Unpublish")
@login_required
def unpublish_question(question_id):
    success = Question.unpublish(question_id)

    if success:
        return redirect(url_for("views.question_list"))

    else:
        return error_html()


def error_html():
    return "<h1>An error occurred whilst processing the last request." \
           "Please go back on your browser to return to site<h1>"
