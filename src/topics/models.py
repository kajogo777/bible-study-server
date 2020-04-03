from django.db import models
from smart_selects.db_fields import ChainedForeignKey
from bible.models import BibleBook, BibleChapter, BibleVerse


class Topic(models.Model):
    title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        unique=True
    )
    intro_text = models.TextField(
        max_length=1000,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title


class TopicReading(models.Model):
    topic = models.ForeignKey(
        'topics.Topic',
        on_delete=models.PROTECT,
        blank=False,
        null=False
    )
    index = models.PositiveIntegerField(
        blank=False,
        null=False,
        db_index=True
    )
    book = models.ForeignKey(
        BibleBook,
        on_delete=models.PROTECT,
        blank=False,
        null=False
    )
    chapter = ChainedForeignKey(
        BibleChapter,
        chained_field='book',
        chained_model_field='book',
        show_all=False,
        on_delete=models.PROTECT, blank=False, null=False)
    start_verse = ChainedForeignKey(
        BibleVerse,
        chained_field='chapter',
        chained_model_field='chapter',
        show_all=False,
        related_name='start_reading',
        on_delete=models.PROTECT, blank=False, null=False)
    end_verse = ChainedForeignKey(
        BibleVerse,
        chained_field='chapter',
        chained_model_field='chapter',
        show_all=False,
        related_name='end_reading',
        on_delete=models.PROTECT, blank=False, null=False)
    bible_study_text = models.TextField(
        max_length=1000,
        blank=True,
        null=True
    )

    class Meta:
        unique_together = [['topic', 'index']]

    def __str__(self):
        if self.index == 1:
            return '1st'
        if self.index == 2:
            return '2nd'
        if self.index == 3:
            return '3rd'
        return f'{self.index}th'


class TopicGroup(models.Model):
    topic = models.ForeignKey(
        'topics.Topic',
        on_delete=models.PROTECT,
        blank=False,
        null=False
    )
    group = models.ForeignKey(
        'users.Group',
        on_delete=models.PROTECT,
        blank=False,
        null=False
    )
    bible_study_channel = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    class Meta:
        unique_together = [['topic', 'group']]


class TopicUser(models.Model):
    topic = models.ForeignKey(
        'topics.Topic',
        on_delete=models.PROTECT,
        blank=False,
        null=False
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        blank=False,
        null=False
    )
    reading_index = models.PositiveIntegerField(
        blank=False,
        null=False,
    )

    class Meta:
        unique_together = [['topic', 'user']]
