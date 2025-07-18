from django import template
import html

register = template.Library()

@register.filter
def truncate_pixels(text, max_pixels=999):
    """
    Truncates a string to approximately `max_pixels` visual width.
    Pixel-Simulation: breite Buchstaben zählen mehr.
    """
    if not isinstance(text, str):
        return text

    weights = {
        'wide': 'WMQGOBDU',  # ca. 10–12px
        'medium': 'ABCDEFHIKLNPRSTXYZ',  # ca. 8–10px
        'narrow': 'acegijlmnoqrstuvwxz',  # ca. 5–7px
        'narrowest': '.,:;|!il\'"[]{}()',  # ca. 2–4px
        'digits': '0123456789',  # ca. 7–9px
    }

    def char_weight(c):
        if c in weights['wide']:
            return 12
        elif c in weights['medium']:
            return 9
        elif c in weights['digits']:
            return 8
        elif c in weights['narrow']:
            return 6
        elif c in weights['narrowest']:
            return 4
        else:
            return 7  # default

    total = 0
    result = ""
    for c in text:
        total += char_weight(c)
        if total > max_pixels:
            result += "..."
            break
        result += c

    return html.escape(result)
