from django.urls import path
from . import views

urlpatterns = [
    path('mainapp/', views.mainapp, name='mainapp'),
]