from decimal import Decimal, InvalidOperation

from django import template

register = template.Library()


@register.filter
def miles(value):
    """Format a number with Colombian thousands separators (periods)."""
    try:
        number = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return value
    rendered = f"{number:,.0f}"
    return rendered.replace(",", ".")
