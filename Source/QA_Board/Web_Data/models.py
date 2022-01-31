import wmgtss_qa
from dataclasses import dataclass
import datetime
import time

@dataclass
class Comment:
    id: int
    description: str
    date_created: datetime.datetime
    parent: int = None


@dataclass
class Question:

    id: int
    title: str
    description: str
    answer: str
    date_created: datetime.datetime
    published: bool
    comments: list = None

    @staticmethod
    def get_question_by_id(question_id):
        for question in wmgtss_qa.get_posts_by_user():
            if question.id == question_id:
                return question
        return None


class Model:

    def __init__(self, user_id, role):
        self.user_id = user_id
        self.role = role
        self.questions = []
        self.update()

    def update(self):

        self.questions = [
            Question(
                question['post_id'], question['post_title'], question['post_description'], question['post_answer'],
                question['post_created'], question['post_published']
            )
            for question
            in wmgtss_qa.get_posts_by_user(self.user_id)
        ]

        for question in self.questions:
            question.comments = [
                Comment(
                    comment['comment_id'], comment['comment_description'], comment['comment_created'],
                    comment['parent_id'])
                for comment
                in wmgtss_qa.get_post_comments(question.id)
            ]