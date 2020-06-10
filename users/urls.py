from django.urls import path
from django.conf.urls import include
from .views import profile_update, profile_view, createCompanyProfile

urlpatterns = [
    path('update/', profile_update, name='profile_update'),
    path('view/', profile_view, name='profile_view'),
    path('CompanyProfile/create', createCompanyProfile, name='createCompanyProfile'),
    ]
