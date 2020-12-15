from django.utils import timezone


def get_year_start():
    today = timezone.localtime(timezone.now()).date()

    year_start = timezone.datetime(year=today.year - 1, month=9, day=1)
    if today.month >= 9:
        year_start = timezone.datetime(year=today.year, month=9, day=1)

    return year_start


def get_days_since_year_start():
    today = timezone.localtime(timezone.now()).date()

    year_start = timezone.datetime(year=today.year - 1, month=9, day=1).date()
    if today.month >= 9:
        year_start = timezone.datetime(year=today.year, month=9, day=1).date()

    return (today - year_start).days + 1
