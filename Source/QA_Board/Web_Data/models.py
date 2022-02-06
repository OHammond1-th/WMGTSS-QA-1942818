from . import wmgtss_qa
from flask_login import UserMixin
from dataclasses import dataclass
import datetime as dt


# Helper function to avoid having runtime errors about parameters not being correct
def protect_construct(class_type, arguments):
    try:
        return class_type(*arguments)
    except TypeError as e:
        print("Error in protect_construct function: ", e)
        return None


pc = protect_construct


@dataclass
class Course:
    ident: int
    name: str
    start: dt.datetime
    end: dt.datetime

    @staticmethod
    def get_by_id(course_id):
        return pc(Course, wmgtss_qa.get_course_by_id(course_id))


@dataclass
class User(UserMixin):
    ident: int
    role: int
    username: str
    password: str
    firstname: str
    lastname: str
    date_of_birth: dt.datetime
    last_interaction: dt.datetime
    created: dt.datetime

    def get_id(self):
        return str(self.ident)

    def get_classes(self):
        return [course for course in wmgtss_qa.get_users_enrollments(self.get_id())]

    @staticmethod
    def get_by_id(user_id):
        return pc(User, wmgtss_qa.get_user(user_id))

    @staticmethod
    def get_by_username(username):
        return pc(User, wmgtss_qa.get_user_by_username(username))

    @staticmethod
    def get_all_students():
        return [pc(User, result) for result in wmgtss_qa.get_users_by_role("student")]


@dataclass
class Question:

    ident: int
    course: int
    author: int
    title: str
    description: str
    answer: str
    date_created: dt.datetime
    published: bool
    publishable: bool

    @staticmethod
    def create_question(course_id, author_id, title, description, publishable):
        return wmgtss_qa.insert_into_posts(course_id, author_id, title, description, publishable)

    @staticmethod
    def get_class_questions(class_id):
        return [pc(Question, result) for result in wmgtss_qa.get_posts_by_class(class_id)]

    @staticmethod
    def get_public_questions(classes):
        all_questions = []
        for course in classes:
            all_questions += Question.get_class_questions(course)

        return all_questions

    @staticmethod
    def get_private_questions(user_id):
        return [pc(Question, result) for result in wmgtss_qa.get_posts_by_user(user_id)]

    @staticmethod
    def get_question_by_id(question_id):
        return pc(Question, wmgtss_qa.get_post(question_id))


@dataclass
class Comment:
    ident: int
    post: int
    author: int
    parent_comment: int
    description: str
    date_created: dt.datetime

    children = []

    @staticmethod
    def create_comment(post_id, author_id, description, parent_id=None):
        return wmgtss_qa.insert_into_comments(post_id, author_id, description, parent_id)

    @staticmethod
    def get_post_comments(post_id):
        comments = [pc(Comment, result) for result in wmgtss_qa.get_post_comments(post_id)]
        comment_tree = []

        for comment in comments:
            if comment.parent_comment is None:
                comment.children = comment.get_comment_children(comments)
                comment_tree.append(comment)

        return comment_tree

    def get_comment_children(self, comment_list):

        children = []

        for comment in comment_list:
            if comment.parent_comment == self.ident:
                comment.children = comment.get_comment_children(comment_list)
                children.append(comment)

        return children
