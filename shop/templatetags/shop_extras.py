from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def sum_item_prices(items):
    """Calculate the total price of all items in a queryset"""
    total = Decimal('0.00')
    for item in items:
        total += item.product.price * item.quantity
    return total
