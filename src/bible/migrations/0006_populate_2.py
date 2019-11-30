import json
from django.db import migrations
from bible.utils import ar_book_name


def populate_en_books(apps, schema_editor):
    BibleBook = apps.get_model('bible', 'BibleBook')
    BibleChapter = apps.get_model('bible', 'BibleChapter')
    BibleVerse = apps.get_model('bible', 'BibleVerse')

    with open('bible/data/en_nkjv.json', mode='r', encoding='utf-8-sig') as en_nkjv:
        en_nkjv_data = json.load(en_nkjv)

        for _, book in enumerate(en_nkjv_data['books']):
            name = book['name']
            chapters = book['chapters']

            book_record = BibleBook.objects.get(name=ar_book_name[name])
            book_record.name_en = name
            book_record.save()

            for chapter in chapters:
                chapter_index = chapter['num']
                verses = chapter['verses']
                chapter_record = BibleChapter.objects.get(
                    book=book_record, index=chapter_index)

                for verse in verses:
                    verse_index = verse['num']
                    verse_text = verse['text']
                    verse_record = BibleVerse.objects.get(
                        chapter=chapter_record, index=verse_index)
                    verse_record.text_en = verse_text
                    verse_record.save()


class Migration(migrations.Migration):

    dependencies = [
        ('bible', '0005_add_text_en'),
    ]

    operations = [
        migrations.RunPython(populate_en_books),
    ]
