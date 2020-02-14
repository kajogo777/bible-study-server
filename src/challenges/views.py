from users.models import Response
from users.authentication import CodeAuthentication, IsAuthenticated
from rest_framework import viewsets, serializers, pagination
from django_filters import rest_framework as filters
from .models import Challenge, Answer
from bible.serializers import BibleVerseSerializer
from bible.models import BibleVerse
from django.utils import timezone
from django.core.cache import cache
from rest_framework.response import Response as HttpResponse


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
        # user = self.context['request'].user

        # try:
        #     response_obj = Response.objects.get(user=user, challenge=challenge)
        #     response = ResponseSerializer(response_obj).data
        # except Response.DoesNotExist:
        #     response = None

        if challenge.active_date >= timezone.localtime(timezone.now()).date():
            answers = RedactedAnswerSerializer(
                challenge.answer_set, many=True).data
        else:
            answers = AnswerSerializer(
                challenge.answer_set, many=True).data

        verses = BibleVerse.objects.filter(
            chapter=challenge.start_verse.chapter, index__gte=challenge.start_verse.index, index__lte=challenge.end_verse.index)

        scripture_verse_text = [verse.text for verse in verses]
        scripture_verse_text_en = [verse.text_en for verse in verses]
        scripture_verse_indexes = [verse.index for verse in verses]

        if challenge.start_verse.id == challenge.end_verse.id:
            verse_range = challenge.start_verse.index
            verse_range_en = challenge.start_verse.index
        else:
            verse_range = "{}-{}".format(
                challenge.end_verse.index, challenge.start_verse.index
            )
            verse_range_en = "{}-{}".format(
                challenge.start_verse.index, challenge.end_verse.index
            )

        scripture_reference = "{}:{} {}".format(
            verse_range, challenge.start_verse.chapter.index, challenge.start_verse.chapter.book.name)
        scripture_reference_en = "{} {}:{}".format(
            challenge.start_verse.chapter.book.name_en, challenge.start_verse.chapter.index, verse_range_en)

        today = timezone.localtime(timezone.now()).date()

        return {
            'id': challenge.id,
            'question': challenge.question,
            'answers': answers,
            'active': challenge.active_date == today,
            'expired': challenge.active_date < today,
            'active_date': challenge.active_date.strftime('%Y-%m-%d'),
            'scripture': {
                'verse_indexes': scripture_verse_indexes,
                'verse_text': scripture_verse_text,
                'verse_text_en': scripture_verse_text_en,
                'chapter': challenge.start_verse.chapter.index,
                'book': challenge.start_verse.chapter.book.name,
                'book_en': challenge.start_verse.chapter.book.name_en,
                'reference': scripture_reference,
                'reference_en': scripture_reference_en
            },
            # 'response': response,
            'reward': {
                'name': challenge.reward_name,
                'color': challenge.reward_color,
                'score': challenge.reward_score,
            },
        }


# class StandardLimitPagination(pagination.LimitOffsetPagination):
#     default_limit = 60
#     max_limit = 60


class ChallengesViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = (CodeAuthentication,)
    permission_classes = (IsAuthenticated,)

    serializer_class = ChallengeSerializer
    # filter_backends = (filters.DjangoFilterBackend,)
    # filterset_fields = ('group', 'active_date')
    # pagination_class = StandardLimitPagination

    def get_queryset(self):
        today = timezone.localtime(timezone.now()).date()
        user = self.request.user
        return Challenge.objects.filter(
            group=user.group,
            active_date__lte=today,
            # active_date__month__in=[today.month, today.month-1]
        ).order_by('-active_date')

    def list(self, request):
        user = self.request.user
        today = timezone.localtime(timezone.now()).date()
        cache_key = f'{today.day}-{user.group.id}'

        challenges = cache.get(cache_key)

        if challenges is None:
            response = super(ChallengesViewSet, self).list(request)
            if response.status_code == 200:
                cache.set(cache_key, response.data, timeout=60*60*2)
                challenges = response.data
            else:
                return response

        for index, challenge in enumerate(challenges):
            challenge_id = challenge['id']
            try:
                response_obj = Response.objects.get(
                    user=user, challenge__id=challenge_id)
                serialized_response = ResponseSerializer(response_obj).data
            except Response.DoesNotExist:
                serialized_response = None
            challenge['response'] = serialized_response
            challenges[index] = challenge

        return HttpResponse({'results': challenges})
