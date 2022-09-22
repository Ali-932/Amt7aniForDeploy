from typing import List

from ninja import Router
from Home.schemas import SubjectsOut, FourOFourOut, StageOut, StagesOut
from Home.models import Stage, Subjects, Profile
from config import status

subject_router = Router(tags=['Subject'])


@subject_router.get('/get_stages',response={
    200:List[StagesOut],
    404:FourOFourOut
})
def get_stages(request):
    result = []
    for t in Stage.objects.all():
        if t.type == 'لا يوجد':
            result.append({
                'id': t.id,
                'stage': t.stages
            })
        else:
            result.append({
                'id': t.id,
                'stage': t.stages.split(' ')[0] + ' ' + t.type
            })

    return status.OK_200, result

@subject_router.get('/get_default_subject',response={
    200: List[SubjectsOut],
    404: FourOFourOut

})
def get_defualt_subjects(request):
    try:
        st=Profile.objects.get(user_id=request.auth['user_id']).stage.get_subjects()
    except Stage.DoesNotExist:
        return status.NOT_FOUND_404, {'detail': 'stage does not exist'}
    except Profile.DoesNotExist:
        return status.NOT_FOUND_404, {'detail': 'profile does not exist'}
    except Subjects.DoesNotExist:
        return status.NOT_FOUND_404, {'detail': 'subject does not exist'}
    result = []
    for a in st:
        result.append({
            'subject': a, 'quiz_count': a.get_quizzes_count()
        })

    return status.OK_200, result


@subject_router.get("/get_subjects", response={
    200: List[SubjectsOut],
    404: FourOFourOut
})
def get_subjects(request, stage_id: int):
    try:
        st = Stage.objects.get(id=stage_id).get_subjects()
    except Stage.DoesNotExist:
        return status.NOT_FOUND_404, {'detail': 'stage does not exist'}
    except Subjects.DoesNotExist:
        return status.NOT_FOUND_404, {'detail': 'subject does not exist'}
    result = []
    for a in st:
        result.append({
            'subject': a, 'quiz_count': a.get_quizzes_count()
        })

    return status.OK_200, result
