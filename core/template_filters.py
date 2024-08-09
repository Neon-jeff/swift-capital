# coding=utf-8
from django.template.defaulttags import register



@register.filter(name='lookup')
def get_item(dictionary, key):
    return f'{int(dictionary.get(key))}.00'
