from users.models import Response
from users.authentication import CodeAuthentication, IsAuthenticated
from rest_framework import viewsets, serializers, pagination
from django_filters import rest_framework as filters
from .models import Challenge, Answer
from bible.serializers import BibleVerseSerializer
from bible.models import BibleVerse
from django.utils import timezone


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ('id', 'answer')


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'text', 'correct')


class RedactedAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'text')


class ChallengeSerializer(serializers.BaseSerializer):
    def to_representation(self, challenge):
        user = self.context['request'].user

        try:
            response_obj = Response.objects.get(user=user, challenge=challenge)
            response = ResponseSerializer(response_obj).data
        except Response.DoesNotExist:
            response = None

        if challenge.active_date >= timezone.localtime(timezone.now()).date():
            answers = RedactedAnswerSerializer(
                challenge.answer_set, many=True).data
        else:
            answers = AnswerSerializer(
                challenge.answer_set, many=True).data

        verses = BibleVerse.objects.filter(
            chapter=challenge.start_verse.chapter, index__gte=challenge.start_verse.index, index__lte=challenge.end_verse.index)

        scripture_verse_text = [verse.text for verse in verses]
        scripture_verse_indexes = [verse.index for verse in verses]

        if challenge.start_verse.id == challenge.end_verse.id:
            verse_range = challenge.start_verse.index
        else:
            verse_range = "{}-{}".format(challenge.start_verse.index,
                                         challenge.end_verse.index)
        scripture_reference = "{}:{} {}".format(
            challenge.start_verse.chapter.index, verse_range, challenge.start_verse.chapter.book.name)

        return {
            'id': challenge.id,
            'question': challenge.question,
            'answers': answers,
            'active_date': challenge.active_date.strftime('%Y-%m-%d'),
            'scripture': {
                'verse_indexes': scripture_verse_indexes,
                'verse_text': scripture_verse_text,
                'chapter': challenge.start_verse.chapter.index,
                'book': challenge.start_verse.chapter.book.name,
                'reference': scripture_reference,
            },
            'response': response,
            'reward': {
                'name': challenge.reward_name,
                'color': challenge.reward_color,
            },
        }


class StandardLimitPagination(pagination.LimitOffsetPagination):
    default_limit = 10
    max_limit = 50


class ChallengesViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = (CodeAuthentication,)
    permission_classes = (IsAuthenticated,)

    serializer_class = ChallengeSerializer
    # filter_backends = (filters.DjangoFilterBackend,)
    # filterset_fields = ('group', 'active_date')
    pagination_class = StandardLimitPagination

    def get_queryset(self):
        today = timezone.localtime(timezone.now()).date()
        user = self.request.user
        return Challenge.objects.filter(group=user.group, active_date__lte=today).order_by('-active_date')
