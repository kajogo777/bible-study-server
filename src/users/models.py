from django.db import models
from django.utils.crypto import get_random_string
from challenges.models import Challenge, Answer
from smart_selects.db_fields import ChainedForeignKey
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator


def generate_code():
    code = get_random_string(length=10)
    return code


class Group(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return "{}".format(self.name)


class Class(models.Model):
    name = models.CharField(
        max_length=30,
        default="",
        blank=False, null=False
    )

    def __str__(self):
        return self.name


class AdminUser(AbstractUser):
    PRIMARY_1 = 1
    PRIMARY_2 = 2
    PRIMARY_3 = 3
    PRIMARY_4 = 4
    PRIMARY_5 = 5
    PRIMARY_6 = 6
    PREPARATORY_1 = 7
    PREPARATORY_2 = 8
    PREPARATORY_3 = 9
    SECONDARY_1 = 10
    SECONDARY_2 = 11
    SECONDARY_3 = 12
    UNIVERSITY = 13
    OTHER = 100
    service_group = models.ForeignKey(
        'users.Group', on_delete=models.PROTECT, blank=True, null=True, related_name='service_group')
    service_class = models.ForeignKey(
        'users.Class', on_delete=models.PROTECT, blank=True, null=True, related_name='service_class')
    service_grade = models.IntegerField(
        choices=[
            (OTHER, "Other"),
            (PRIMARY_1, "Primary 1"),
            (PRIMARY_2, "Primary 2"),
            (PRIMARY_3, "Primary 3"),
            (PRIMARY_4, "Primary 4"),
            (PRIMARY_5, "Primary 5"),
            (PRIMARY_6, "Primary 6"),
            (PREPARATORY_1, "Preparatory 1"),
            (PREPARATORY_2, "Preparatory 2"),
            (PREPARATORY_3, "Preparatory 3"),
            (SECONDARY_1, "Secondary 1"),
            (SECONDARY_2, "Secondary 2"),
            (SECONDARY_3, "Secondary 3"),
            (UNIVERSITY, "University"),
        ],
        blank=True, null=True
    )

    class Meta:
        verbose_name = 'Admin User'
        verbose_name_plural = 'Admin Users'


class User(models.Model):
    PRIMARY_1 = 1
    PRIMARY_2 = 2
    PRIMARY_3 = 3
    PRIMARY_4 = 4
    PRIMARY_5 = 5
    PRIMARY_6 = 6
    PREPARATORY_1 = 7
    PREPARATORY_2 = 8
    PREPARATORY_3 = 9
    SECONDARY_1 = 10
    SECONDARY_2 = 11
    SECONDARY_3 = 12
    UNIVERSITY = 13
    OTHER = 100

    group = models.ForeignKey(
        'users.Group', on_delete=models.PROTECT, blank=False, null=False, related_name='user_group')
    group_class = models.ForeignKey(
        'users.Class', on_delete=models.PROTECT, blank=True, null=True, related_name='user_class')
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
    grade = models.IntegerField(
        choices=[
            (OTHER, "Other"),
            (PRIMARY_1, "Primary 1"),
            (PRIMARY_2, "Primary 2"),
            (PRIMARY_3, "Primary 3"),
            (PRIMARY_4, "Primary 4"),
            (PRIMARY_5, "Primary 5"),
            (PRIMARY_6, "Primary 6"),
            (PREPARATORY_1, "Preparatory 1"),
            (PREPARATORY_2, "Preparatory 2"),
            (PREPARATORY_3, "Preparatory 3"),
            (SECONDARY_1, "Secondary 1"),
            (SECONDARY_2, "Secondary 2"),
            (SECONDARY_3, "Secondary 3"),
            (UNIVERSITY, "University"),
        ],
        blank=False, null=True
    )

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
