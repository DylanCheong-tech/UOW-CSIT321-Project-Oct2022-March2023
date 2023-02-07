# eventowner_urls.py

from django.urls import path

from ..views import eventowner_views as views

urlpatterns = [
    path('createaccount', views.EventOwnerCreateAccountView.as_view()),
    path('getOTP', views.EventOwnerCreateAccountGetOTP.as_view()),
    path('login', views.EventOwnerLogin.as_view()),
    path('logout', views.EventOwnerLogout.as_view()),
    path('homepage', views.EventOwnerHomePage.as_view()),
    path('createevent', views.EventOwnerCreateNewVoteEvent.as_view()),
    path('updateevent/<int:eventNo>', views.EventOwnerUpdateVoteEvent.as_view()),
    path('viewevent/<int:eventNo>', views.EventOwnerViewVoteEvent.as_view()),
    path('deleteevent/<int:eventNo>', views.EventOwnerDeleteVoteEvent.as_view()),
    path('confirmevent/<int:eventNo>', views.EventOwnerConfirmVoteEvent.as_view()),
    path('event/finalresult/<int:eventNo>', views.EventOwnerViewVoteEventFinalResult.as_view()),
    path('event/finalresult/publish/<int:eventNo>', views.EventOwnerPublishVoteEventFinalResult.as_view()),
    path('completedevent', views.EventOwnerViewCompletedVoteEvents.as_view()),
    path('ongoingevent', views.EventOwnerViewOnGoingVoteEvents.as_view()),
    path('about', views.EventOwnerAbout.as_view())
]