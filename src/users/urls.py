from rest_framework import routers
from .views import UsersViewSet, ResponseViewSet, GroupsViewSet, UserScoreViewSet, deeplink_helper
from django.urls import path

router = routers.SimpleRouter()
router.register(r'users', UsersViewSet, basename='user')
router.register(r'groups', GroupsViewSet)
router.register(r'responses', ResponseViewSet)
router.register(r'score', UserScoreViewSet, basename='score')


urlpatterns = [
    path('deeplink/<code>', deeplink_helper),
]
