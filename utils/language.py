"""
utils/language.py
------------------
تشخیص ساده زبان فارسی یا انگلیسی بر اساس محدوده کاراکترهای یونیکد.
"""

PERSIAN_RANGE = range(0x0600, 0x06FF + 1)


def detect_language(text: str) -> str:
    """اگر پیام حاوی حروف فارسی/عربی باشد 'fa' برمی‌گرداند، در غیر این صورت 'en'."""
    for char in text:
        if ord(char) in PERSIAN_RANGE:
            return "fa"
    return "en"