# voter_urls.py

from django.urls import path

from ..views import voter_views as views

urlpatterns = [
    path('vote', views.VoterVoteForm.as_view()),
    path('finalresult', views.VoterViewFinalResult.as_view()),
]