from django.contrib import admin
from django.urls import path, include
from ninja import NinjaAPI
from restauth.api import auth_router
from restauth import views

api = NinjaAPI(
    title='Amt7ani',
    version='0.2',
    description='Amt7ani api.',
    csrf=True,
)
api.add_router('auth/', auth_router)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('chaining/', include('smart_selects.urls')),
    path('_nested_admin/', include('nested_admin.urls')),
    path('accounts/', include('allauth.urls')),
    path("api/", api.urls),
    path("email_confirmatin/", views.confirm_em, name='emailC')

]
