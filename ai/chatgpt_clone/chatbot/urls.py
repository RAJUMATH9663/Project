from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),          # http://127.0.0.1:8000/
    path('chat/', views.chat_api, name='chat'), # http://127.0.0.1:8000/api/chat/
]