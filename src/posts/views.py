from users.authentication import CodeAuthentication, IsAuthenticated
from rest_framework import viewsets, serializers, pagination
from .models import Post, PostGroup
from django.utils import timezone


class ConcisePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'summary', 'active_date')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'summary', 'active_date', 'text')


class StandardLimitPagination(pagination.LimitOffsetPagination):
    default_limit = 10
    max_limit = 30


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = (CodeAuthentication,)
    permission_classes = (IsAuthenticated,)

    pagination_class = StandardLimitPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return ConcisePostSerializer
        else:
            return PostSerializer

    def get_queryset(self):
        user = self.request.user
        today = timezone.localtime(timezone.now()).date()
        return Post.objects.filter(postgroup__group=user.group, active_date__lte=today,)
