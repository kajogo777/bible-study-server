import csv
from django.db import migrations

BOOK_NAME_EN = "Wisdom of Solomon"
BOOK_NAME_AR = "حكمة سليمان"

def populate_book(apps, schema_editor):
    BibleBook = apps.get_model('bible', 'BibleBook')
    BibleChapter = apps.get_model('bible', 'BibleChapter')
    BibleVerse = apps.get_model('bible', 'BibleVerse')
    
    book_record = BibleBook()
    book_record.name = BOOK_NAME_AR
    book_record.name_en = BOOK_NAME_EN
    book_record.save()
    with open('bible/data/wisdom_of_solomon.csv', newline='', encoding='utf-8-sig') as csvfile:
        verses = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        current_chapter_index = 0
        current_chapter = None
        for verse in verses:
            if int(verse["chapter"]) > current_chapter_index:
                current_chapter = BibleChapter()
                current_chapter.index = int(verse["chapter"])
                current_chapter.book = book_record
                current_chapter.save()
                current_chapter_index += 1

            verse_record = BibleVerse()
            verse_record.index = int(verse["verse"])
            verse_record.chapter = current_chapter
            verse_record.text = verse["ar"]
            verse_record.text_en = verse["en"]
            verse_record.save()


class Migration(migrations.Migration):

    dependencies = [
        ('bible', '0010_populate_6_sirach'),
    ]

    operations = [
        migrations.RunPython(populate_book),
    ]
