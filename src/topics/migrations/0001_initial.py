# Generated by Django 2.2.10 on 2020-04-03 17:56

from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0004_auto_20191011_1107'),
        ('bible', '0006_populate_2'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('intro_text', models.TextField(blank=True, max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TopicUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reading_index', models.PositiveIntegerField()),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='topics.Topic')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.User')),
            ],
            options={
                'unique_together': {('topic', 'user')},
            },
        ),
        migrations.CreateModel(
            name='TopicReading',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.PositiveIntegerField(db_index=True)),
                ('bible_study_text', models.TextField(blank=True, max_length=1000, null=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bible.BibleBook')),
                ('chapter', smart_selects.db_fields.ChainedForeignKey(chained_field='book', chained_model_field='book', on_delete=django.db.models.deletion.PROTECT, to='bible.BibleChapter')),
                ('end_verse', smart_selects.db_fields.ChainedForeignKey(chained_field='chapter', chained_model_field='chapter', on_delete=django.db.models.deletion.PROTECT, related_name='end_reading', to='bible.BibleVerse')),
                ('start_verse', smart_selects.db_fields.ChainedForeignKey(chained_field='chapter', chained_model_field='chapter', on_delete=django.db.models.deletion.PROTECT, related_name='start_reading', to='bible.BibleVerse')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='topics.Topic')),
            ],
            options={
                'unique_together': {('topic', 'index')},
            },
        ),
        migrations.CreateModel(
            name='TopicGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bible_study_channel', models.CharField(blank=True, max_length=100, null=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.Group')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='topics.Topic')),
            ],
            options={
                'unique_together': {('topic', 'group')},
            },
        ),
    ]
