from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
    path('', views.home, name='index_page'),  
=======
    path('', views.home, name='index_page'),
    path("signup/", views.register, name="signup"),
    path("login/", views.login_view, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.user_logout, name="logout"),  
    path('churn/',views.home, name="index_page"),
    path('segment/',views.segment, name = "segment"),
>>>>>>> 4d785195 (added html and css)
]
