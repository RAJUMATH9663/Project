from django.contrib import admin
from django.urls import path
from voteapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.vote, name='home'),   # ✅ ADD THIS
    path('vote/', views.vote, name='vote'),
    path('result/', views.result, name='result'),
]