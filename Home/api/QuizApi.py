from typing import List

from django.db.models import Count
from ninja import Router
from Home.models import Chapters, Quiz, Question, Stage, UserQuizzes, choices, Subjects, Profile
from Home.schemas import FourOFourOut, QuizOut, QuizListin, QuizList
from config import status

quiz_router = Router(tags=['Quiz'])


@quiz_router.post('/get_defualt_quiz_lists', response={
    200: List[QuizList],
    404: FourOFourOut
})
def get_defualt_quiz_lists(request, sub: int):
    try:
        st = Profile.objects.get(user_id=request.auth['user_id']).stage
        sb = Subjects.objects.get(id=sub)
        qz = Quiz.objects.filter(subject=sb, stage=st)
    except:
        return status.NOT_FOUND_404, {'detail': 'input does not exist'}
    result = []
    for q in qz:
        result.append({
            'name': q.name,
            'chapter': list(Chapters.objects.filter(quiz=q)),
            'q_num': q.q_num,
            'timer': q.timer,
            'id':q.id
        })
    return status.OK_200, result

@quiz_router.post('/get_quiz_lists', response={
    200: List[QuizList],
    404: FourOFourOut
})
def get_quiz_lists(request, sub: int,stage:int):
    try:
        st = Stage.objects.get(id=stage)
        sb = Subjects.objects.get(id=sub)
        qz = Quiz.objects.filter(subject=sb, stage=st)
    except:
        return status.NOT_FOUND_404, {'detail': 'input does not exist'}
    result = []
    for q in qz:
        result.append({
            'name': q.name,
            'chapter': list(Chapters.objects.filter(quiz=q)),
            'q_num': q.q_num,
            'timer': q.timer,
            'id':q.id
        })
        print(result)
    return status.OK_200, result

@quiz_router.get('/get_quiz', response={
    200: QuizOut,
    404: FourOFourOut
})
def get_quiz(request, quizid: int):
    try:
        qz = Quiz.objects.get(id=quizid)
        q = qz.get_questions()

    except Quiz.DoesNotExist:
        return status.NOT_FOUND_404, {'detail': 'input does not exist'}
    result = []
    for a in q:
        result.append({
            'Questions': a,
            'Choices': list(a.get_choices())
        })
    q_count = qz.get_questions_count()
    if q_count >= qz.q_num:
        q_count = qz.q_num
    return status.OK_200, {'quiz': result, 'timer': qz.timer, 'q_num': q_count}

#
# @quiz_router.post('/get_quiz_all', response={
#     200: QuizOut,
#     404: FourOFourOut
# })
# def get_quiz_all(request, quizin: QuizListin):
#     try:
#         st = Stage.objects.get(id=quizin.stage)
#         sb = Subjects.objects.get(id=quizin.subject)
#         q = Question.objects.prefetch_related('choices_question').filter(quiz__subject=sb, quiz__stage=st).order_by('?')
#     except:
#         return status.NOT_FOUND_404, {'detail': 'input does not exist'}
#     result = []
#     q_count = Question.objects.filter(quiz__subject=sb, quiz__stage=st).aggregate(count=Count('id'))['count']
#     if q_count >= 100:
#         q_count = 100
#     for a in q[:100]:
#         result.append({
#             'Questions': a,
#             'Choices': list(a.get_choices())
#         })
#     return status.OK_200, {'quiz': result, 'timer': "60:00", 'q_num': q_count}
