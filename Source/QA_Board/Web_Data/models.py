from . import wmgtss_qa
from flask_login import UserMixin
from dataclasses import dataclass
import datetime as dt


def protect_construct(class_type, arguments):
    """
    Helper function that is able to unload the values provided by a queries result fetch
    :param class_type: The class of which an instance will be constructed
    :param arguments: The arguments to use in construction
    :return: The created instance
    """
    print(class_type, arguments)
    try:
        return class_type(*arguments)
    except TypeError as e:
        print("Error in protect_construct function: ", e)
        return None


# Shortening of the function name
pc = protect_construct

# Global variable to allow outside files to manipulate the value
db = wmgtss_qa.DB_singleton("WMGTSS_QA", "web_client", "default")


@dataclass
class Course:
    """
    Class that mimics a row of the courses table in the WMGTSS database
    """

    ident: int
    name: str
    start: dt.datetime
    end: dt.datetime

    @staticmethod
    def get_by_id(course_id):
        """
        Get an instance by the courses id
        :param course_id: The course id
        :return: The instance created
        """
        return pc(Course, db.get_course_by_id(course_id))

    @staticmethod
    def get_by_name(course_name):
        """
        Get an instance by the course name
        :param course_name: The course name
        :return: The instance created
        """
        return pc(Course, db.get_course_by_name(course_name))

    @staticmethod
    def get_random():
        """
        Get a random course
        :return: The instance created
        """
        return pc(Course, db.get_random_course())


@dataclass
class User(UserMixin):
    """
    Class that mimics a row of the users table in the WMGTSS database
    """

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
        """
        Find out if a user is elevated
        :return: Elevation status
        """
        return db.get_user_elevation(self.ident)

    def update_interaction(self):
        """
        Update the last interaction field of a user
        :return: Success status
        """

        # Only do this if the user is not elevated
        if not self.is_elevated():
            self.last_interaction = dt.datetime.today().date()

        return db.update_table_row("users", ["user_interacted_last"], [self.last_interaction], self.ident)

    def hasnt_interacted_today(self):
        """
        Find out if the user has already interacted within the last 24hrs
        :return: Their interaction status
        """
        today = dt.date.today()

        # if the user has never interacted then it is true
        if self.last_interaction is None:
            return True

        time_period = today - self.last_interaction

        # if the time since last interaction is greater than 24hrs then this is true
        if time_period.days > 1:
            return True
        return False

    def get_id(self):
        """
        Get a string version of the users id
        :return: Users id
        """
        return str(self.ident)

    def get_classes(self):
        """
        Get all classes that the user is enrolled in
        :return: All classes enrolled in
        """
        return [Course.get_by_id(enrollment[0]) for enrollment in db.get_users_enrollments(self.get_id())]

    @staticmethod
    def set_password_by_id(user_id, password):
        """
        Changes a users password (Requires prior hashing)
        :param user_id: Users id
        :param password: Users new password
        :return: Success status
        """
        return db.set_user_password(user_id, password)

    @staticmethod
    def get_by_id(user_id):
        """
        Get an instance of the user by their id
        :param user_id: Users id
        :return: User instance
        """
        return pc(User, db.get_user(user_id))

    @staticmethod
    def get_by_username(username):
        """
        Get an instance of the user by their username
        :param username: Users username
        :return: User instance
        """
        return pc(User, db.get_user_by_username(username))

    @staticmethod
    def get_all_students():
        """
        Returns all users within the database
        :return: All user instances
        """
        return [pc(User, result) for result in db.get_users_by_role("student")]

    @staticmethod
    def get_random():
        """
        Returns a random user from the database
        :return: User instance
        """
        return pc(User, db.get_random_user())


@dataclass
class Question:

    """
    Class that mimics a row of the posts table in the WMGTSS database
    """

    ident: int
    course: int
    author: int
    title: str
    description: str
    answer: str
    date_created: dt.datetime
    publishable: bool
    published: bool

    @staticmethod
    def create_question(course_id, author_id, title, description, publishable):
        """
        Provide all the data needed to create a new question
        :param course_id: The course that this question is associated with
        :param author_id: The user that this question is associated with
        :param title: The title of the question
        :param description: The description of the question
        :param publishable: Whether this question will be publishable
        :return: The success status
        """
        return db.insert_into_posts(course_id, author_id, title, description, publishable)[0]

    @staticmethod
    def get_class_questions(class_id):
        """
        Gets a question instance by its class association
        :param class_id: The class to get questions from
        :return: The questions instance list
        """
        return [pc(Question, result) for result in db.get_posts_by_class(class_id)]

    @staticmethod
    def get_public_questions(classes):
        """
        Get all questions that have been published
        :param classes: All classes that the caller is allowed to see
        :return: All questions from requested classes that are published
        """
        all_questions = []

        # for each class call get questions and append concatenate them to the final question list
        for course in classes:
            all_questions += Question.get_class_questions(course)

        # Only return a question if it is published
        return [question for question in all_questions if question.published]

    @staticmethod
    def get_private_questions(user_id):
        """
        Get all questions associated with a user
        :param user_id: The users is
        :return: The question instance list
        """
        return [pc(Question, result) for result in db.get_posts_by_user(user_id)]

    @staticmethod
    def get_question_by_id(question_id):
        """
        Get a question by its id
        :param question_id: The question id
        :return: The question instance
        """
        return pc(Question, db.get_post(question_id))

    @staticmethod
    def provide_answer(question_id, answer):
        """
        Give the desired question an answer
        :param question_id: The question id
        :param answer: the answer to give
        :return: Success status
        """
        return db.update_post_with_answer(question_id, answer)

    @staticmethod
    def publish(question_id):
        """
        Set a question to published
        :param question_id: The question id
        :return: Success status
        """
        return db.set_publish_state(question_id, True)

    @staticmethod
    def unpublish(question_id):
        """
        Set a question to not published
        :param question_id: The question id
        :return: Success status
        """
        return db.set_publish_state(question_id, False)

    @staticmethod
    def delete(question_id):
        """
        Delete a question by its id
        :param question_id: The question id
        :return: Success status
        """
        return db.delete_from_posts(question_id)


@dataclass
class Comment:
    """
    Class that mimics a row of the comments table in the WMGTSS database
    """
    ident: int
    post: int
    author: int
    parent_comment: int
    description: str
    date_created: dt.datetime

    # A variable that will store the child comments of this comment for use later
    children = []

    @staticmethod
    def create_comment(question_id, author_id, description, parent_id=None):
        """
        Provide all the data needed to create a comment
        :param question_id: The question it will be associated with
        :param author_id: The user it will be associated with
        :param description: The content of the comment
        :param parent_id: The parent comment if one exists
        :return: The id of the new comment
        """
        return db.insert_into_comments(question_id, author_id, description, parent_id)

    @staticmethod
    def soft_delete_comment(comment_id):
        """
        Deletes the content of a comment but allows the instance to remain in order to preserve comment structure
        :param comment_id: The comments id
        :return: Success status
        """
        return db.delete_comment(comment_id)

    @staticmethod
    def get_post_comments(post_id):
        """
        Gets all the comments associated with a post and structures them into a tree of parent and child comments
        :param post_id: The post id
        :return: All comment instances with no parent associated that have their children stored within
        """
        comments = [pc(Comment, result) for result in db.get_post_comments(post_id)]
        comment_tree = []

        print(comments)

        for comment in comments:
            # If this is a base comment
            if comment.parent_comment is None:
                # Go through all the comments and find this comments children
                comment.children = comment.get_comment_children(comments)

                # Add this comment to the comment tree
                comment_tree.append(comment)

        return comment_tree

    def get_comment_children(self, comment_list):
        """
        Finds all comments that have this instance as their parent
        :param comment_list: All comment instances
        :return: A list of all the children of this comment instance
        """
        children = []

        for comment in comment_list:
            # If a comments parent is this comment
            if comment.parent_comment == self.ident:
                # Gather that child comments children
                comment.children = comment.get_comment_children(comment_list)
                # Add the child comment to the parents child list
                children.append(comment)

        # Give the child list back to the parent
        return children
