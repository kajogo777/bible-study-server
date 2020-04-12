from bible.utils import get_scripture
from users.authentication import CodeAuthentication, IsAuthenticated
from rest_framework import viewsets, serializers, pagination
from .models import Topic, TopicReading, TopicGroup, TopicUser


class TopicReadingSerializer(serializers.ModelSerializer):
    scripture = serializers.SerializerMethodField()

    def get_scripture(self, obj):
        return get_scripture(obj.start_verse, obj.end_verse)

    class Meta:
        model = TopicReading
        fields = ('id', 'topic', 'index', 'bible_study_text', 'scripture')


class ConciseTopicReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicReading
        fields = ('id', 'topic', 'index')


class TopicSerializer(serializers.ModelSerializer):
    # readings = serializers.PrimaryKeyRelatedField(
    #     source='topicreading_set', many=True, read_only=True)
    readings = ConciseTopicReadingSerializer(
        source='topicreading_set', many=True, read_only=True)

    class Meta:
        model = Topic
        fields = ('id', 'title', 'type', 'intro_text', 'readings')


class StandardLimitPagination(pagination.LimitOffsetPagination):
    default_limit = 10
    max_limit = 30


class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = (CodeAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = TopicSerializer

    pagination_class = StandardLimitPagination

    def get_queryset(self):
        user = self.request.user
        return Topic.objects.filter(topicgroup__group=user.group)


class ReadingViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = (CodeAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = TopicReadingSerializer

    pagination_class = StandardLimitPagination

    def get_queryset(self):
        return TopicReading.objects.filter(topic=self.kwargs['topics_pk'])
