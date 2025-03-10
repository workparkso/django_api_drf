from . import views
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView


app_name = "users"

urlpatterns = [
    path('create/', views.user_create, name='user_create'),  
    
    
]