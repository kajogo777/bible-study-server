# from rest_framework import routers
# from .views import TopicViewSet

# router = routers.SimpleRouter()
# router.register(r'topics', TopicViewSet, basename='topics')

from rest_framework_nested import routers
from .views import TopicViewSet, ReadingViewSet

router = routers.SimpleRouter()
router.register(r'topics', TopicViewSet, basename='topic')

topics_nested_router = routers.NestedSimpleRouter(
    router, r'topics', lookup='topics')
topics_nested_router.register(r'readings', ReadingViewSet,
                              base_name='topics-readings')
