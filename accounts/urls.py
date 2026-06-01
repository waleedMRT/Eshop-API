from django.urls import path
from .views import register , current_user
urlpatterns = [
    path('register/' , register , name='register' ),
    path('current_user/' , current_user , name='current_user' ),
]