from flask import Blueprint, request, redirect, url_for, render_template
import models

views = Blueprint('views', __name__)

@views.route('/Login')
def login():

    #TODO: Create secure login portal to get user data

@views.route('/')
def home():
    return "<h1>Test<h1>"

@views.route('/Questions')
def question_list():

    #TODO: Get list of Public and Private questions

    return render_template("question_list.html",
                           public_questions=Questions["public"],
                           private_questions=Questions["private"]
                           )

@views.route('/Questions/<int:question_id>')
def question_page(question_id):
    question = models.Question.get_question_by_id(question_id)
    if question:
        return render_template("question_page.html", question=question)
    else:
        return redirect(url_for("question_list"))