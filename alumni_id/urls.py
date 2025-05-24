from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload-background/', views.upload_background, name='upload_background'),
    path('backgrounds/', views.background_list, name='background_list'),
    path('register/', views.register_alumni, name='register_alumni'),
    path('alumni/', views.alumni_list, name='alumni_list'),
    path('alumni/<int:alumni_id>/id-card/', views.view_id_card, name='view_id_card'),
] 