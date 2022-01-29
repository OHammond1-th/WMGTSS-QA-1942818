import wmgtss_qa
from dataclasses import dataclass
import datetime
import time

@dataclass
class Question:

    title: str
    description: str
    answer: str
    date_created: datetime.datetime
    published: bool