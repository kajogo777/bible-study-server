from rest_framework import serializers
from .models import BibleBook, BibleChapter, BibleVerse


class BibleVerseSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        return {
            'verse_index': obj.index,
            'chapter_index': obj.chapter.index,
            'book_name': obj.chapter.book.name
        }

