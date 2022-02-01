from flask import Blueprint, request, redirect, url_for, render_template
from models import Question

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
    return redirect(url_for('login'))


@views.route('/Questions')
def question_list():
    questions_public = Question.get_public_questions()
    questions_private = Question.get_private_questions()

    return render_template("question_list.html",
                           public_questions=questions_public,
                           private_questions=questions_private
                           )


@views.route('/Questions', methods=['POST'])
def question_list():
    _id = request.form.get("post_id")
    if _id:
        return redirect(url_for('question_page', question_id=_id))


@views.route('/Questions/<int:question_id>')
def question_page(question_id):

    if question:
        return render_template("question_page.html", question=question, comments=comments)
    else:
        return redirect(url_for("question_list"))
