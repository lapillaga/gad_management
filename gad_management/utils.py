import locale
from datetime import datetime, date

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')


def get_formatted_date(to_format_date: date):
    """
    Get the formatted date for the application
    """
    return to_format_date.strftime('%d de %B de %Y')
