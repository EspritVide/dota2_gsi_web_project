from django.urls import path
from . import views

urlpatterns = [
    path('reciever/', views.gsi_reciever, name='gsi_reciever'),
]
