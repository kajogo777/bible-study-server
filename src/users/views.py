from rest_framework import viewsets, serializers, mixins
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response as HttpResponse
from challenges.models import Challenge
from .models import User, Group, Response
from .authentication import CodeAuthentication, IsOwner, IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from django.core.cache import cache


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


class UserScoreViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = (CodeAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request, format=None):
        user = request.user
        today = timezone.localtime(timezone.now()).date()
        last_30_days = today - timedelta(days=30)

        user_challenges = Challenge.objects.filter(
            group=user.group,
            active_date__lt=today
        )
        user_challenges_last_30_days = user_challenges.filter(
            active_date__gt=last_30_days
        )
        user_attempted_responses = Response.objects.filter(
            user=user,
        )
        user_attempted_responses_last_30_days = user_attempted_responses.filter(
            challenge__active_date__gt=last_30_days
        )
        user_correct_responses = user_attempted_responses.filter(
            answer__correct=True
        )
        user_correct_responses_last_30_days = user_correct_responses.filter(
            challenge__active_date__gt=last_30_days
        )

        total_challenges = user_challenges.count()
        total_challenges_last_30_days = user_challenges_last_30_days.count()

        total_correct = user_correct_responses.count()
        total_correct_last_30_days = user_correct_responses_last_30_days.count()

        total_attempted = user_attempted_responses.count()
        total_attempted_last_30_days = user_attempted_responses_last_30_days.count()

        total_score = user_correct_responses.aggregate(
            Sum('challenge__reward_score')
        ).get('challenge__reward_score__sum', 0)
        total_score_last_30_days = user_correct_responses_last_30_days.aggregate(
            Sum('challenge__reward_score')
        ).get('challenge__reward_score__sum', 0)

        return HttpResponse({
            'total_challenges': total_challenges,
            'total_attempted': total_attempted,
            'total_correct': total_correct,
            'total_score': total_score,

            'total_challenges_last_30_days': total_challenges_last_30_days,
            'total_attempted_last_30_days': total_attempted_last_30_days,
            'total_correct_last_30_days': total_correct_last_30_days,
            'total_score_last_30_days': total_score_last_30_days,
        })
