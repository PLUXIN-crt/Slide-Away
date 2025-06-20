from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiplica value por arg"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def add_shipping(value, modalidad):
    """Agrega costo de despacho si la modalidad es 'despacho'"""
    try:
        if modalidad == 'despacho':
            return float(value) + 5000
        return float(value)
    except (ValueError, TypeError):
        return value
