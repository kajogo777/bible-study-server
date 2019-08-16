from rest_framework import routers
from .views import UsersViewSet, ResponseViewSet, GroupsViewSet

router = routers.SimpleRouter()
router.register(r'users', UsersViewSet, basename='user')
router.register(r'groups', GroupsViewSet)
router.register(r'responses', ResponseViewSet)
