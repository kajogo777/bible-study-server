from django.db import models
from django.core.validators import MinValueValidator


class BibleBook(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return "{}".format(self.name)


class BibleChapter(models.Model):
    book = models.ForeignKey(
        BibleBook, on_delete=models.CASCADE, blank=False, null=False)
    index = models.PositiveIntegerField(blank=False, null=False, db_index=True)

    class Meta:
        ordering = ['book', 'index']

    def __str__(self):
        return "{}".format(self.index)


class BibleVerse(models.Model):
    chapter = models.ForeignKey(
        BibleChapter, on_delete=models.CASCADE, blank=False, null=False)
    index = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    text = models.CharField(max_length=700, blank=False, null=False)

    class Meta:
        ordering = ['chapter', 'index']

    def __str__(self):
        return "{}".format(self.index)
