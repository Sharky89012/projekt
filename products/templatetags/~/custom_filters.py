from django import template
import re

register = template.Library()

@register.filter
def remove_repeats(value):
    words = value.split()
    seen = set()
    result = []
    for word in words:
        clean_word = re.sub(r'[^\wäöüÄÖÜß-]', '', word.lower())
        if clean_word not in seen:
            seen.add(clean_word)
            result.append(word)
    return ' '.join(result)
