from django import template

register = template.Library()


@register.filter
def to_farsi_digit(value: str):
    """
    Method to conver EN digits to Farsi digits.
    """

    if not isinstance(value, str):
        value = str(value)

    farsi_digits = {
        '0': '۰',
        '1': '۱',
        '2': '۲',
        '3': '۳',
        '4': '۴',
        '5': '۵',
        '6': '۶',
        '7': '۷',
        '8': '۸',
        '9': '۹',
    }

    return ''.join(farsi_digits.get(digit, digit) for digit in value)
