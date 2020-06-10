from django.conf.urls import url
from django.urls import path
from .views import create_suggestion, suggestion_detail


urlpatterns = [
    path('create/<slug:url>', create_suggestion, name='create_suggestion'),
    path('view/<slug:url>', suggestion_detail, name='suggestion_detail'),
]
