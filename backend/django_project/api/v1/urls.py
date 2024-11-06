from django.urls import include, path
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'games', views.GameViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('get_cfg_file/', views.CfgFileView.as_view(), name='get_cfg_file'),
]
