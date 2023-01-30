# public_urls.py

from django.urls import path

from ..views import public_views as views

urlpatterns = [
    path('', views.MainPublicPage.as_view()),
]