from django.utils.safestring import mark_safe
from django.template import Library
import json
from datetime import date,datetime
register = Library()


@register.filter(is_safe=True)
def js(obj):
    return mark_safe(json.dumps(obj))

@register.filter()
def sub(a, b):
    return a-b

@register.filter()
def date(d):
    dt = datetime.strptime(d[:10], '%Y-%m-%d').strftime('%d %b %Y')
    return dt