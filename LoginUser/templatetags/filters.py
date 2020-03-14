from django import template

register=template.Library()
@register.filter()
def myfilter(num):
    num=str(num)[:4]+"****"+str(num)[8:]
    return num