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