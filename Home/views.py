from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from Home.models import Profile,Stage,Subjects,Chapters,Question,choices


@login_required
def Stage_list(request):
    stage = Stage.objects.all()
    return JsonResponse({'data': [{'id':p.id,'stages': p.stages, 'profile': p.profile} for p in stage]})


@login_required
def Subjects_list(request, St_id):
    kabupaten = Subjects.objects.filter(stage_id=St_id)
    return JsonResponse({'data': [{'id': k.id, 'name': k.name,'stage':k.stage,'type':k.type} for k in kabupaten]})

#
# @login_required
# def kecamatan_list(request, kabupaten_id):
#     kecamatan = Kecamatan.objects.filter(kabupaten_id=kabupaten_id)
#     return JsonResponse({'data': [{'id': k.id, 'name': k.name} for k in kecamatan]})
#
#
# @login_required
# def kelurahan_list(request, kecamatan_id):
#     kelurahan = Kelurahan.objects.filter(kecamatan_id=kecamatan_id)
#     return JsonResponse({'data': [{'id': k.id, 'name': k.name} for k in kelurahan]})
