from django.db import models
from smart_selects.db_fields import ChainedForeignKey
from bible.models import BibleBook, BibleChapter, BibleVerse


class Challenge(models.Model):
    group = models.ForeignKey(
        'users.Group', on_delete=models.PROTECT, blank=False, null=False)

    active_date = models.DateField(
        auto_now=False, auto_now_add=False, blank=False, null=False)

    book = models.ForeignKey(
        BibleBook, on_delete=models.PROTECT, blank=False, null=False)
    chapter = ChainedForeignKey(
        BibleChapter,
        chained_field="book",
        chained_model_field="book",
        show_all=False,
        on_delete=models.PROTECT, blank=False, null=False)
    start_verse = ChainedForeignKey(
        BibleVerse,
        chained_field="chapter",
        chained_model_field="chapter",
        show_all=False,
        related_name='start_challenge',
        on_delete=models.PROTECT, blank=False, null=False)
    end_verse = ChainedForeignKey(
        BibleVerse,
        chained_field="chapter",
        chained_model_field="chapter",
        show_all=False,
        related_name='end_challenge',
        on_delete=models.PROTECT, blank=False, null=False)

    question = models.TextField(max_length=1000, blank=False, null=False)

    reward_color = models.CharField(max_length=10, blank=False, null=False)
    reward_name = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return "{}: {}".format(self.group.name, self.active_date)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Challenge, self).save(*args, **kwargs)


class Answer(models.Model):
    challenge = models.ForeignKey(
        Challenge, on_delete=models.CASCADE, blank=False, null=False)

    text = models.TextField(max_length=1000, blank=False, null=False)
    correct = models.BooleanField(blank=False, null=False, default=False)

    def __str__(self):
        text = self.text
        if self.correct:
            text += " (correct)"
        return text
