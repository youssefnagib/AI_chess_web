from django.urls import path
from . import views

urlpatterns = [
    path('play/', views.chess_view, name='chess_1v1')
]
