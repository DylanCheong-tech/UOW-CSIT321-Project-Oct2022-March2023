from django.urls import path

from . import views 

urlpatterns = [
    path('eventowner/createaccount', views.EventOwnerCreateAccountView.as_view()),
    path('eventowner/getOTP', views.EventOwnerCreateAccountGetOTP.as_view()),
    path('eventowner/login', views.EventOwnerLogin.as_view()),
    path('eventowner/logout', views.EventOwnerLogout.as_view()),
    path('eventowner/homepage', views.EventOwnerHomePage.as_view()),
    path('eventowner/createevent', views.EventOwnerCreateNewVoteEvent.as_view()),
    path('eventowner/updateevent/<int:eventNo>', views.EventOwnerUpdateVoteEvent.as_view()),
    path('eventowner/viewevent/<int:eventNo>', views.EventOwnerViewVoteEvent.as_view()),
    path('eventowner/deleteevent/<int:eventNo>', views.EventOwnerDeleteVoteEvent.as_view())
]