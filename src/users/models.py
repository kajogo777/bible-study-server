from django.db import models
from django.utils.crypto import get_random_string
from challenges.models import Challenge, Answer
from smart_selects.db_fields import ChainedForeignKey
from django.contrib.auth.models import AbstractUser


def generate_code():
    code = get_random_string(length=10)
    return code


class Group(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return "{}".format(self.name)


class AdminUser(AbstractUser):
    service_group = models.ForeignKey(
        'users.Group', on_delete=models.PROTECT, blank=True, null=True, related_name='service_group')

    class Meta:
        verbose_name = 'Admin User'
        verbose_name_plural = 'Admin Users'


class User(models.Model):
    group = models.ForeignKey(
        'users.Group', on_delete=models.PROTECT, blank=False, null=False, related_name='user_group')
    name = models.CharField(max_length=50, blank=False, null=False)
    date_of_birth = models.DateField(
        auto_now=False, auto_now_add=False, blank=False, null=False)
    gender = models.CharField(
        max_length=7,
        choices=(
            ('Male', 'Male'),
            ('Female', 'Female')
        )
    )
    code = models.CharField(max_length=10, unique=True,
                            blank=False, null=False, default=generate_code)

    def is_authenticated(self):
        return True


class Response(models.Model):
    challenge = models.ForeignKey(
        'challenges.Challenge', on_delete=models.CASCADE, blank=False, null=False)
    # answer = models.ForeignKey(
    #     'challenges.Answer', on_delete=models.CASCADE, blank=False, null=False)
    answer = ChainedForeignKey(
        Answer,
        chained_field="challenge",
        chained_model_field="challenge",
        show_all=False,
        on_delete=models.CASCADE, blank=False, null=False)

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        unique_together = [['user', 'challenge']]
