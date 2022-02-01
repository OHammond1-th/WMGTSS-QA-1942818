import wmgtss_qa
from dataclasses import dataclass
import datetime as dt
import time

@dataclass
class User:
    id: int
    role: int
    firstname: str
    lastname: str
    date_of_birth: dt.datetime
    last_interaction: dt.datetime
    created: dt.datetime

    @staticmethod
    def get_all_students():
        return [User(*result) for result in wmgtss_qa.get_users_by_role("student")]


@dataclass
class Question:

    id: int
    title: str
    description: str
    answer: str
    date_created: dt.datetime
    published: bool
    publishable: bool

    @staticmethod
    def get_public_questions():
        return [Question(*result) for result in wmgtss_qa.get_published_posts()]

    @staticmethod
    def get_private_questions(user_id):
        return [Question(*result) for result in wmgtss_qa.get_posts_by_user(user_id)]


@dataclass
class Comment:
    id: int
    post: int
    author: int
    parent_comment: int
    description: str
    date_created: dt.datetime

    @staticmethod
    def get_post_comments(post_id):
        comments = [{'object': result, 'level': 0} for result in wmgtss_qa.get_post_comments(post_id)]

        for comment in comments:

            if comment['object'].parent_comment is None:
                break

            for parent in comments:

                if parent['object'].id == comment['object'].parent_comment:
                    comment['level'] = parent['level'] + 1
                    break

        return comments
