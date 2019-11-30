from django.db import models
from django.core.validators import MinValueValidator


class BibleBook(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    name_en = models.CharField(max_length=100, blank=True, null=True)

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
    text_en = models.CharField(max_length=700, blank=True, null=True)

    class Meta:
        ordering = ['chapter', 'index']

    def __str__(self):
        return "{}".format(self.index)
