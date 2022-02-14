import traceback

from flask import Blueprint, request, redirect, url_for, render_template, flash, escape
from flask_login import login_required, logout_user, current_user
from .models import Course, User, Question, Comment

# Blueprint variable to be referenced by our app
views = Blueprint('views', __name__)


@views.route('/')
def home():
    """
    Entry point of the website main page designed to redirect the user to the question board
    :return: The question board url
    """
    return redirect(url_for('views.question_list'))


@views.route('/Logout')
@login_required
def logout():
    """
    Logs out the user session and returns the user to the home, this will actually return the user to the given login
    page but for modularity we do not want to reference another blueprint here
    :return:
    """

    logout_user()

    return redirect(url_for('views.home'))


@views.route('/Questions', methods=['GET', 'POST'])
@login_required
def question_list():
    """
    Main page that contains a list of all the currently available questions and the question asking form
    :return: html for the question page
    """
    try:
        # get the current courses the user is enrolled in
        courses = current_user.get_classes()

        # if the user has arrived on the page render the questions
        if request.method == 'GET':
            # get users elevation status and the ids of the courses gathered earlier
            elevated = current_user.is_elevated()
            course_ids = [course.ident for course in courses]

            # attempt to get the questions that the user would need to see otherwise display no questions available
            try:
                questions_public = Question.get_public_questions(course_ids)
                questions_private = Question.get_private_questions(current_user.get_id())
            except TypeError:
                questions_public = []
                questions_private = []

            # render the question_list template with the variables gathered earlier
            return render_template("question_list.html",
                                   elevated=elevated,
                                   courses=courses,
                                   public_questions=questions_public,
                                   private_questions=questions_private
                                   )

        # if the user has submitted a question attempt to create a new qeustion in the database
        if request.method == 'POST':
            # get the data from the form
            title = escape(request.form['title'])
            description = escape(request.form['description'])
            course_input = escape(request.form['selected-course'])
            publishable = True if request.form.get('publishable') == "on" else False

            # get the course instance that was selected in the form
            for course in courses:
                if course_input.strip() == course.name:
                    course_input = course.ident

            # create a new question if all of the data required is available
            if title and description and course_input and publishable is not None and current_user.hasnt_interacted_today():
                question_id = str(Question.create_question(course_input, current_user.ident, title, description, publishable))

                # tell the databse a user needs to have their interaction updated
                current_user.update_interaction()

                # send the user to the newly created question
                return redirect(url_for('views.question_page', question_id=question_id))

            flash("Submission failed due to missing field")
            return redirect(url_for("views.question_list"))

        else:
            return "<h1>405: Method not allowed.</h1>"

    except TypeError as e:
        print(e)
        return "<h2>You are not enrolled or an error has occurred. " \
               "Please contact the system administrator if there is a problem <h2>"


@views.route('/Questions/<int:question_id>', methods=['GET', 'POST'])
@login_required
def question_page(question_id):
    """
    The page that displays the selected question
    :param question_id: The question id
    :return: The question page html
    """
    # if the user has landed on the page render the template
    if request.method == 'GET':
        # get the question and any meta data that is associated with it
        question = Question.get_question_by_id(question_id)
        course = Course.get_by_id(question.course)
        author = User.get_by_id(question.author)

        # get the current user to provide the comment creator if necessary
        user = current_user
        comments = Comment.get_post_comments(question_id)

        # if the question was found render it other wise redirect to the question list
        if question:
            return render_template("question_page.html", question=question,
                                   author=author, user=user, comments=comments, course=course)
        else:
            return redirect(url_for("views.question_list"))

    # if the user has submitted a comment create it using the hidden form
    if request.method == 'POST':
        # get the comment data to be used
        parent = escape(request.form['comment-parent'])
        text = escape(request.form['comment-text'])

        # if the comment has no parent then set its parent value to null
        if int(parent) == -1:
            parent = "NULL"

        # make sure the comment has text to be used as its content
        if text:
            # create the comment and assert that it was created
            success = Comment.create_comment(question_id, current_user.ident, text, parent)

            if not success:
                return error_html()

        return redirect(url_for("views.question_page", question_id=question_id))

    else:
        return "<h1>405: Method not allowed.</h1>"


@views.route("/Questions/<int:question_id>/Deleting")
@login_required
def delete_question(question_id):
    """
    Deletes a given question from the database
    :param question_id: The question id
    :return: The question list url
    """
    success = Question.delete(question_id)

    if success:
        return redirect(url_for("views.question_list"))

    else:
        return error_html()


@views.route("/Questions/<int:question_id>/Comments/<int:comment_id>/Deleting")
@login_required
def delete_comment(question_id, comment_id):
    """
    Delete a given comment from the database but return to the currently viewed question
    :param question_id: Question to return to
    :param comment_id: The comment id
    :return: Question to return to url
    """
    Comment.soft_delete_comment(comment_id)
    return redirect(url_for("views.question_page", question_id=question_id))


@views.route("/Questions/<int:question_id>/Answer", methods=['GET', 'POST'])
@login_required
def answer_question(question_id):
    """
    Sends a user to the questions answer page
    :param question_id: The question id
    :return: The question answer html
    """
    # if the user is elevated and has landed on this page render the answer html with the current answer
    if current_user.is_elevated() and request.method == 'GET':
        return render_template("question_answer.html", question=Question.get_question_by_id(question_id))

    # if the user has submitted the answer change it and return to the question page
    if current_user.is_elevated() and request.method == 'POST':
        answer = escape(request.form['answer'])

        # Default for empty answer is None so it must be converted from string to NoneType
        answer = answer if answer is not "None" else None
        Question.provide_answer(question_id, answer)

    return redirect(url_for("views.question_page", question_id=question_id))


@views.route("/Questions/<int:question_id>/Publish")
@login_required
def publish_question(question_id):
    """
    Publish a question
    :param question_id: The question id
    :return: The question list page
    """
    success = Question.publish(question_id)

    if success:
        return redirect(url_for("views.question_list"))

    else:
        return error_html()


@views.route("/Question/<int:question_id>/Unpublish")
@login_required
def unpublish_question(question_id):
    """
    Unpublish a question
    :param question_id: The question id
    :return: The question list page
    """
    success = Question.unpublish(question_id)

    if success:
        return redirect(url_for("views.question_list"))

    else:
        return error_html()


def error_html():
    return "<h1>An error occurred whilst processing the last request." \
           "Please go back on your browser to return to site<h1>"
