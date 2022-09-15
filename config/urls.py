from django.contrib import admin
from django.urls import path, include
from ninja import NinjaAPI

from Home.api import subject_router
from Home.api.ProfileApi import profile_router
from Home.api.QuizApi import quiz_router
from Home.api.Quiz_profileApi import quiz_log_router
from restauth.api import auth_router
from restauth import views
from restauth.authorization import AuthBearer

api = NinjaAPI(
    title='Amt7ani',
    version='0.2',
    description='Amt7ani api.',
    csrf=True,
    auth=AuthBearer()
)
api.add_router('auth/', auth_router)
api.add_router('quizLog/', quiz_log_router)
api.add_router('subjects/',subject_router)
api.add_router('Quiz/',quiz_router)
api.add_router('profile',profile_router)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('chaining/', include('smart_selects.urls')),
    path('_nested_admin/', include('nested_admin.urls')),
    path('accounts/', include('allauth.urls')),
    path("api/", api.urls),
    path("email_confirmatin/", views.confirm_em, name='emailC'),
    path('__debug__/', include('debug_toolbar.urls')),
    path('silk/', include('silk.urls', namespace='silk'))
]
#For removing authall from admin
from django.contrib import admin
from allauth.socialaccount.models import SocialToken, SocialAccount, SocialApp
from allauth.account.models import EmailAddress
admin.site.unregister(SocialToken)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialApp)
admin.site.unregister(EmailAddress)
