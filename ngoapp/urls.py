from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("valid", views.valid, name="valid"),
    path("<str:ngoo>/details", views.details, name="details"),
    path("listngo", views.listt, name="listt"),
    path("signupuser", views.signupuser, name="signupuser"),
    path("loginuser", views.loginuser, name="loginuser"),

]
