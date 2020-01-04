from rest_framework import viewsets, serializers
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated
from .models import User, Group, Response
from .authentication import CodeAuthentication, IsOwner, IsAuthenticated
from django.utils import timezone


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'group', 'gender', 'date_of_birth')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


class ResponseSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Response
        fields = ('id', 'user', 'challenge', 'answer')

    def validate(self, attrs):
        challenge = attrs.get('challenge')
        today = timezone.localtime(timezone.now()).date()
        if today != challenge.active_date:
            raise serializers.ValidationError(
                'Responding to challenge should be done on its active date.')
        return attrs


class UsersViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = (CodeAuthentication,)
    permission_classes = (IsAuthenticated,)

    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class GroupsViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = (CodeAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ResponseViewSet(viewsets.ModelViewSet):
    authentication_classes = (CodeAuthentication,)
    permission_classes = (IsAuthenticated, IsOwner,)

    queryset = Response.objects.all()
    serializer_class = ResponseSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('challenge',)
