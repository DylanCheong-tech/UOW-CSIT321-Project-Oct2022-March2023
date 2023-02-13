# public_urls.py

from django.urls import path

from ..views import public_views as views

urlpatterns = [
    path('', views.MainPublicPage.as_view(),name="main_page"),
    path('about', views.AboutPublicPage.as_view()),
]