from django.utils.text import slugify
from transliterate import translit


def slugify_text(text: str) -> str:
    return slugify(translit(text, 'ru', reversed=True))
