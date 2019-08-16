from rest_framework import routers
from .views import ChallengesViewSet

router = routers.SimpleRouter()
router.register(r'challenges', ChallengesViewSet, basename='challenge')
