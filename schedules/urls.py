from django.urls import path
from . import views

app_name = "schedules"

urlpatterns = [
    path('', views.schedule_list, name='schedule-list'), 
    path('create/', views.schedule_create, name='schedule-create'),  
    
    
]