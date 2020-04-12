from rest_framework import routers
from .views import UsersViewSet, ResponseViewSet, GroupsViewSet, UserScoreViewSet

router = routers.SimpleRouter()
router.register(r'users', UsersViewSet, basename='user')
router.register(r'groups', GroupsViewSet)
router.register(r'responses', ResponseViewSet)
router.register(r'score', UserScoreViewSet, basename='score')
