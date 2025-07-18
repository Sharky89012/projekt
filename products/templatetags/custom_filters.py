from django import template
import re
from django.utils.html import strip_tags
from django.utils.text import Truncator
register = template.Library()

@register.filter
def remove_repeats(value):
    words = re.split(r'[\s,.-]+', value)  # trennt auch bei Kommas, Punkten, Bindestrichen
    seen = set()
    result = []
    original_words = value.split()  # um die originale Wortform zu behalten

    i = 0
    for word in words:
        normalized = word.lower()
        if normalized not in seen:
            seen.add(normalized)
            # nehme das ursprüngliche Wort aus original_words an derselben Stelle
            if i < len(original_words):
                result.append(original_words[i])
            else:
                result.append(word)
        i += 1

    return ' '.join(result)



@register.filter
def removespecial(value):
    # Entfernt Unicode-Sonderzeichen wie mathematisch fette Buchstaben etc.
    return re.sub(r'[\u1D400-\u1D7FF]', '', value)

@register.filter
def seo_description(value, length=150):
    clean = strip_tags(value)                       # HTML entfernen
    clean = removespecial(clean)                   # Sonderzeichen entfernen
    return Truncator(clean).chars(length, truncate='...')