from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('list/', views.todo_list, name='todo-list'), 
    
    path('checkbox/', views.todo_checkbox, name='todo-checkbox'),  

