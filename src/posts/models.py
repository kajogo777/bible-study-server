from django.db import models
from ckeditor.fields import RichTextField


class Post(models.Model):
    title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        unique=True
    )
    active_date = models.DateField(
        auto_now=False, auto_now_add=False, blank=False, null=False)
    summary = models.TextField(
        max_length=200,
        blank=False,
        null=False,
    )
    text = RichTextField(
        config_name='default',
        blank=False,
        null=False
    )

    def __str__(self):
        return self.title


class PostGroup(models.Model):
    post = models.ForeignKey(
        'posts.Post',
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

    class Meta:
        unique_together = [['post', 'group']]


class PostUser(models.Model):
    post = models.ForeignKey(
        'posts.Post',
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
    rating = models.PositiveIntegerField(
        blank=True,
        null=True,
        choices=[
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 5)
        ]
    )

    class Meta:
        unique_together = [['post', 'user']]
