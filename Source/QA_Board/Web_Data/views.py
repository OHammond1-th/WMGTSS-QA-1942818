from flask import Blueprint, request, redirect, url_for, render_template
import models

views = Blueprint('views', __name__)


@views.route('/Login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")

    if request.method == 'POST':
        # TODO: Verify user input for secure login
        pass

    else:
        return "<h1>405: Method not allowed.</h1>"


@views.route('/')
def home():
    return "<h1>Test<h1>"


@views.route('/Questions')
def question_list():
    # TODO: Get list of Public and Private questions
    questions_public = None
    questions_private = None

    return render_template("question_list.html",
                           public_questions=questions_public,
                           private_questions=questions_private
                           )


@views.route('/Questions/<int:question_id>')
def question_page(question_id):
    question = models.Question.get_question_by_id(question_id)
    if question:
        return render_template("question_page.html", question=question)
    else:
        return redirect(url_for("question_list"))
