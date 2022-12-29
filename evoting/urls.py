from django.urls import path

from . import views 

urlpatterns = [
    path('eventowner/createaccount', views.EventOwnerCreateAccountView.as_view()),
]