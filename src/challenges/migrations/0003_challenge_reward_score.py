# Generated by Django 2.2.1 on 2020-01-03 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0002_auto_20190914_0008'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='reward_score',
            field=models.PositiveIntegerField(default=0),
        ),
    ]