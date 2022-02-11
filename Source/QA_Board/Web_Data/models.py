from . import wmgtss_qa
from flask_login import UserMixin
from dataclasses import dataclass
import datetime as dt


# Helper function to avoid having runtime errors about parameters not being correct
def protect_construct(class_type, arguments):
    print(class_type, arguments)
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
        return pc(Course, wmgtss_qa.db.get_course_by_id(course_id))


@dataclass
class User(UserMixin):
    ident: int
    role: int
    username: str
    password: str
    firstname: str
    lastname: str
    date_of_birth: dt.date
    last_interaction: dt.date
    created: dt.date

    def is_elevated(self):
        return wmgtss_qa.db.get_user_elevation(self.ident)

    def update_interaction(self):

        if not self.is_elevated():
            self.last_interaction = dt.datetime.today().date()

        return wmgtss_qa.db.update_table_row("users", ["user_interacted_last"], [self.last_interaction], self.ident)

    def hasnt_interacted_today(self):
        today = dt.date.today()

        if self.last_interaction is None:
            return True

        time_period = today - self.last_interaction

        if time_period.days > 1:
            return True
        return False

    def get_id(self):
        return str(self.ident)

    def get_classes(self):
        return [Course.get_by_id(enrollment) for enrollment in wmgtss_qa.db.get_users_enrollments(self.get_id())]

    @staticmethod
    def get_by_id(user_id):
        return pc(User, wmgtss_qa.db.get_user(user_id))

    @staticmethod
    def get_by_username(username):
        return pc(User, wmgtss_qa.db.get_user_by_username(username))

    @staticmethod
    def get_all_students():
        return [pc(User, result) for result in wmgtss_qa.db.get_users_by_role("student")]


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
        return wmgtss_qa.db.insert_into_posts(course_id, author_id, title, description, publishable)[0][0]

    @staticmethod
    def get_class_questions(class_id):
        return [pc(Question, result) for result in wmgtss_qa.db.get_posts_by_class(class_id)]

    @staticmethod
    def get_public_questions(classes):
        all_questions = []
        for course in classes:
            all_questions += Question.get_class_questions(course)

        return all_questions

    @staticmethod
    def get_private_questions(user_id):
        return [pc(Question, result) for result in wmgtss_qa.db.get_posts_by_user(user_id)]

    @staticmethod
    def get_question_by_id(question_id):
        return pc(Question, wmgtss_qa.db.get_post(question_id))

    @staticmethod
    def provide_answer(question_id, answer):
        return wmgtss_qa.db.update_question_with_answer(question_id, answer)

    @staticmethod
    def delete(question_id):
        return wmgtss_qa.db.delete_from_questions(question_id)


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
