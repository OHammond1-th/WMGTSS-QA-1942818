import wmgtss_qa
from dataclasses import dataclass
import datetime
import time


@dataclass
class Comment:
    id: int
    description: str
    date_created: datetime.datetime


@dataclass
class Question:

    id: int
    title: str
    description: str
    answer: str
    date_created: datetime.datetime
    published: bool
    comments: list


class Model:

    def __init__(self, user_id, role):
        self.user_id = user_id
        self.role = role
        self.update()

    def update(self):

        self.user_questions = [Question() for question in wmgtss_qa.get_posts_by_user(self.user_id)]

        for question in self.user_questions:
            question.comments = [Comment() for comment in wmgtss_qa.get_post_comments(question.id)]

