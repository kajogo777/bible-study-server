from django.core.cache import cache
from .models import BibleVerse

ar_book_name = {
    'Genesis': 'تكوين',
    'Exodus': 'خروج',
    'Leviticus': 'لاويين',
    'Numbers': 'عدد',
    'Deuteronomy': 'تثنية',
    'Joshua': 'يشوع',
    'Judges': 'قضاة',
    'Ruth': 'راعوث',
    '1 Samuel': '1 صموئيل',
    '2 Samuel': '2 صموئيل',
    '1 Kings': '1 ملوك',
    '2 Kings': '2 ملوك',
    '1 Chronicles': '1 اخبار',
    '2 Chronicles': '2 اخبار',
    'Ezra': 'عزرا',
    'Nehemiah': 'نحميا',
    'Esther': 'استير',
    'Job': 'ايوب',
    'Psalms': 'مزامير',
    'Proverbs': 'امثال',
    'Ecclesiastes': 'جامعة',

    'Song of Songs': 'نشيد الانشاد',
    'Song of Solomon': 'نشيد الانشاد',

    'Isaiah': 'اشعياء',
    'Jeremiah': 'ارميا',
    'Lamentations': 'مراثي',
    'Ezekiel': 'حزقيال',
    'Daniel': 'دانيال',
    'Hosea': 'هوشع',
    'Joel': 'يوئيل',
    'Amos': 'عاموس',
    'Obadiah': 'عوبديا',
    'Jonah': 'يونان',
    'Micah': 'ميخا',
    'Nahum': 'ناحوم',
    'Habakkuk': 'حبقوق',
    'Zephaniah': 'صفنيا',
    'Haggai': 'حجى',
    'Zechariah': 'زكريا',
    'Malachi': 'ملاخي',
    'Matthew': 'متى',
    'Mark': 'مرقس',
    'Luke': 'لوقا',
    'John': 'يوحنا',
    'Acts': 'اعمال',
    'Romans': 'رومية',
    '1 Corinthians': '1 كورنثوس',
    '2 Corinthians': '2 كورنثوس',
    'Galatians': 'غلاطية',
    'Ephesians': 'افسس',
    'Philippians': 'فيلبي',
    'Colossians': 'كولوسي',
    '1 Thessalonians': '1 تسالونيكي',
    '2 Thessalonians': '2 تسالونيكي',
    '1 Timothy': '1 تيموثاوس',
    '2 Timothy': '2 تيموثاوس',
    'Titus': 'تيطس',
    'Philemon': 'فليمون',
    'Hebrews': 'عبرانيين',
    'James': 'يعقوب',
    '1 Peter': '1 بطرس',
    '2 Peter': '2 بطرس',
    '1 John': '1 يوحنا',
    '2 John': '2 يوحنا',
    '3 John': '3 يوحنا',
    'Jude': 'يهوذا',
    'Revelation': 'رؤيا',
}

# en_book_name = {
#      'تكوين': 'Genesis',
#      'خروج': 'Exodus',
#      'لاويين': 'Leviticus',
#      'عدد': 'Numbers',
#      'تثنية': 'Deuteronomy',
#      'يشوع': 'Joshua',
#      'قضاة': 'Judges',
#      'راعوث': 'Ruth',
#      '1 صموئيل': '1 Samuel',
#      '2 صموئيل': '2 Samuel',
#      '1 ملوك': '1 Kings',
#      '2 ملوك': '2 Kings',
#      '1 اخبار': '1 Chronicles',
#      '2 اخبار': '2 Chronicles',
#      'عزرا': 'Ezra',
#      'نحميا': 'Nehemiah',
#      'استير': 'Esther',
#      'ايوب': 'Job',
#      'مزامير': 'Psalms',
#      'امثال': 'Proverbs',
#      'جامعة': 'Ecclesiastes',

#      'نشيد الانشاد': 'Song of Solomon',

#      'اشعياء': 'Isaiah',
#      'ارميا': 'Jeremiah',
#      'مراثي': 'Lamentations',
#      'حزقيال': 'Ezekiel',
#      'دانيال': 'Daniel',
#      'هوشع': 'Hosea',
#      'يوئيل': 'Joel',
#      'عاموس': 'Amos',
#      'عوبديا': 'Obadiah',
#      'يونان': 'Jonah',
#      'ميخا': 'Micah',
#      'ناحوم': 'Nahum',
#      'حبقوق': 'Habakkuk',
#      'صفنيا': 'Zephaniah',
#      'حجى': 'Haggai',
#      'زكريا': 'Zechariah',
#      'ملاخي': 'Malachi',
#      'متى': 'Matthew',
#      'مرقس': 'Mark',
#      'لوقا': 'Luke',
#      'يوحنا': 'John',
#      'اعمال': 'Acts',
#      'رومية': 'Romans',
#      '1 كورنثوس': '1 Corinthians',
#      '2 كورنثوس': '2 Corinthians',
#      'غلاطية': 'Galatians',
#      'افسس': 'Ephesians',
#      'فيلبي': 'Philippians',
#      'كولوسي': 'Colossians',
#      '1 تسالونيكي': '1 Thessalonians',
#      '2 تسالونيكي': '2 Thessalonians',
#      '1 تيموثاوس': '1 Timothy',
#      '2 تيموثاوس': '2 Timothy',
#      'تيطس': 'Titus',
#      'فليمون': 'Philemon',
#      'عبرانيين': 'Hebrews',
#      'يعقوب': 'James',
#      '1 بطرس': '1 Peter',
#      '2 بطرس': '2 Peter',
#      '1 يوحنا': '1 John',
#      '2 يوحنا': '2 John',
#      '3 يوحنا': '3 John',
#      'يهوذا': 'Jude',
#      'رؤيا': 'Revelation',
# }

superscript_map = {
    0: '\u2070',
    1: '\u00B9',
    2: '\u00B2',
    3: '\u00B3',
    4: '\u2074',
    5: '\u2075',
    6: '\u2076',
    7: '\u2077',
    8: '\u2078',
    9: '\u2079',
}


def index_to_superscript(index):
    result = ''
    while index > 0:
        result = superscript_map[index % 10] + result
        index //= 10
    return result


def get_scripture(start_verse, end_verse):
    cache_key = f'scripture:{start_verse.chapter.id}:{start_verse.id}:{end_verse.id}'

    scripture = cache.get(cache_key)

    if scripture is None:
        verses = BibleVerse.objects.filter(
            chapter=start_verse.chapter, index__gte=start_verse.index, index__lte=end_verse.index)

        scripture_verse_text = [verse.text for verse in verses]
        scripture_verse_text_en = [verse.text_en for verse in verses]
        scripture_verse_indexes = [verse.index for verse in verses]

        if start_verse.id == end_verse.id:
            verse_range = start_verse.index
            verse_range_en = start_verse.index
        else:
            verse_range = "{}-{}".format(
                end_verse.index, start_verse.index
            )
            verse_range_en = "{}-{}".format(
                start_verse.index, end_verse.index
            )

        scripture_reference = "{}:{} {}".format(
            verse_range, start_verse.chapter.index, start_verse.chapter.book.name)
        scripture_reference_en = "{} {}:{}".format(
            start_verse.chapter.book.name_en, start_verse.chapter.index, verse_range_en)

        scripture = {
            'verse_indexes': scripture_verse_indexes,
            'verse_text': scripture_verse_text,
            'verse_text_en': scripture_verse_text_en,
            'chapter': start_verse.chapter.index,
            'book': start_verse.chapter.book.name,
            'book_en': start_verse.chapter.book.name_en,
            'reference': scripture_reference,
            'reference_en': scripture_reference_en
        }

        cache.set(cache_key, scripture, timeout=60*60*24*30)

    return scripture
