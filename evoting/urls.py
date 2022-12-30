from django.urls import path

from . import views 

urlpatterns = [
    path('eventowner/createaccount', views.EventOwnerCreateAccountView.as_view()),
    path('eventowner/getOTP', views.EventOwnerCreateAccountGetOTP.as_view()),
    path('eventowner/login', views.EventOwnerLogin.as_view()),
    path('eventowner/homepage', views.EventOwnerHomePage.as_view()),
]