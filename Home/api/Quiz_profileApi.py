from typing import List

from django.contrib.auth import get_user_model
from ninja import Router
from Home.models import Quiz, UserQuizzes, choices, Subjects, UserScoring, Profile,Chapters
from Home.schemas import FourOFourOut, QuizHistoryIn, TwoOO, QuizHistoryOut, AvgNtottal, FourOO
from config import status
User = get_user_model()

quiz_log_router = Router(tags=['quiz_profile'])

@quiz_log_router.post('/post_quiz_history', response={
    404: FourOFourOut,
    200: TwoOO
})
def post_quiz_history(request, quizHin: QuizHistoryIn):
    try:
        user = Profile.objects.get(user_id=request.auth['user_id'])
        quiz = Quiz.objects.get(id=quizHin.quiz_id)

    except User.DoesNotExist:
        return status.NOT_FOUND_404, {'detail': 'User is not registered'}
    UserQuizzes.objects.create(user=user,quiz=quiz, created=quizHin.created,
                               score=quizHin.score)
    return status.OK_200, {'detail': '200'}


@quiz_log_router.get('/get_quizzes_history',response={
    404:FourOFourOut,
    200:List[QuizHistoryOut]
})
def get_quizzes_history(request):
    try:
        user = Profile.objects.get(user_id=request.auth['user_id'])
        uq=UserQuizzes.objects.filter(user=user)
        result=[]
        for a in uq:
            result.append({

                'subject': a.quiz.subject.name, 'chapter': a.quiz.name, 'score': a.score, 'created': str(a.created)
            })
        print(result)
        return status.OK_200,result
    except UserQuizzes.DoesNotExist:
        return status.NOT_FOUND_404, {'detail': 'Quizzes for the user is not registered'}


@quiz_log_router.get('/get_avg_n_total',response={
    404:FourOFourOut,
    200:AvgNtottal,
    400:FourOO
})
def get_avg_n_total(request):
    try:
        user = Profile.objects.get(user_id=request.auth['user_id'])
        us=UserScoring.objects.get(user=user)
    except UserScoring.DoesNotExist:
        return status.NOT_FOUND_404, {'detail': 'User is not registered'}
    try:
        result={
            'avg':us.get_avg_score(),
            'total':us.get_total_quizzes()
        }
    except ZeroDivisionError:
        return status.BAD_REQUEST_400, {'detail': 'Division by zero error'}

    return status.OK_200,result