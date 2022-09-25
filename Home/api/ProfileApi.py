from typing import List

from django.contrib.auth import get_user_model
from ninja import Router
from Home.models import  Profile
from Home.schemas import FourOFourOut, TwoOO, Profileinfo
from config import status

User = get_user_model()

profile_router = Router(tags=['profile'])


@profile_router.post('/update_profile', response={
    200: TwoOO,
    404: FourOFourOut
})
def update_profile(request, updated_info: Profileinfo):
    try:
        Profile.objects.get(user_id=request.auth['user_id']).Update_profile(name=updated_info.name,
                                                                            gender=updated_info.gender,
                                                                            stage_id=updated_info.stage_id)
        return status.OK_200, {'detail': 'profile updated'}
    except:
        return status.BAD_REQUEST_400, {'detail': 'something went wrong'}


@profile_router.get('/profile_info', response={
    200: Profileinfo,
    404: FourOFourOut
})
def get_profile_info(request):
    try:
        p = Profile.objects.get(user_id=request.auth['user_id'])
    except Profile.DoesNotExist:
        return status.NOT_FOUND_404, {'detail': 'profile does not exist'}
    if p.stage.type == 'لا يوجد':
        return status.OK_200, {'name': p.name, 'stage_name': p.stage.stages, 'stage_id': p.stage_id, 'gender': p.gender}
    else:
        return status.OK_200, {'name': p.name, 'stage_name': p.stage.stages.split(' ')[0] + ' ' + p.stage.type,
                               'stage_id': p.stage_id, 'gender': p.gender}
