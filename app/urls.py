from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path("", lambda request: redirect("login")),
    path("signup/", views.register, name="signup"),
    path("login/", views.login_view, name="login"),
    path("dashboard/", views.dashboard, name="mainpage"),
    path("logout/", views.user_logout, name="logout"),  
    path('churn/',views.home, name="index_page"),
    path('segment/', lambda request: redirect('/customer/'), name="segment"),
]
