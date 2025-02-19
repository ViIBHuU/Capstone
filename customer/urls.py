from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('select-columns/', views.select_columns, name='select_columns'),
    path('results/', views.results, name='results'),
    path('cleanup_files/', views.cleanup_files, name='cleanup_files'),
]