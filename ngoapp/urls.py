from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("loginadmin", views.loginadmin, name="loginadmin"),
    # path("pay", views.pay, name="pay"),
    path("adminpanel", views.adminpanel, name="adminpanel"),
    # path("valid", views.valid, name="valid"),
    path("donate", views.donate, name="donate"),
    path("logout", views.logout, name="logout"),
    path("signupngo", views.signupngo, name="signupngo"),
    path("crowdfunding", views.crowdfunding, name="crowdfunding"),
    path("payment", views.payment, name="payment"),
    path("<str:ngoo>/details", views.details, name="details"),
    path("<str:namee>/ngos", views.ngos, name="ngos"),
    path("listngo", views.listt, name="listt"),
    path("signupuser", views.signupuser, name="signupuser"),
    path("loginuser", views.loginuser, name="loginuser"),
    path("<str:id>/passgen", views.passgen, name="passgen"),
]
