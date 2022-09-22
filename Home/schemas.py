from ninja import Schema
from decimal import Decimal
from typing import List


class ProfileOut(Schema):
    name: str
    gender: str
    id: int
    stage: 'StageOut'


class StageOut(Schema):
    stages: str
    type: str


class chapterOut(Schema):
    name: str


class sub(Schema):
    name: str
    id:int
    stage: StageOut


class SubjectsOut(Schema):
    subject: sub
    quiz_count: int




class QuestionOut(Schema):
    questionBody: str
    isProblem: bool
    image: str = None


class ChoicesOut(Schema):
    choiceBody: str
    isCorrect: bool


class Quiz(Schema):
    Questions: QuestionOut
    Choices: List[ChoicesOut]
class QuizOut(Schema):
    quiz:List[Quiz]
    timer:str
    q_num:int
class QuizHistoryOut(Schema):
    subject:str
    chapter:str
    score:str
    created:str

class QuizHistoryIn(Schema):
    quiz_id:int
    created: str
    score:int


class QuizListin(Schema):
    subject: int
    stage:int

class AvgNtottal(Schema):
    avg:int
    total:int

class QuizList(Schema):
    name: str
    chapter: List[chapterOut]
    q_num: int
    timer: str
    id:int
class Profileinfo(Schema):
    name:str
    stage_id:int
    stage_name:str
    gender:str

class StagesOut(Schema):
    id:int
    stage:str

class StageIn(Schema):
    stage: str


class FourOFourOut(Schema):
    detail: str


class TwoOTwo(Schema):
    detail: str


class TwoOO(Schema):
    detail: str


class FourOO(Schema):
    detail: str


class FourOThree(Schema):
    detail: str
