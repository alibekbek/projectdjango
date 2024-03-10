from django import template
from django.db.models import Count

import market.views as views
from market.models import Category, TagPost

register = template.Library()


@register.inclusion_tag('market/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.annotate(total=Count("posts")).filter(total__gt=0)
    return {'cats': cats, 'cat_selected': cat_selected}


@register.inclusion_tag('market/list_tags.html')
def show_all_tags():
    cats = Category.objects.all()
    return {'tags': TagPost.objects.annotate(total=Count("tags")).filter(total__gt=0)}
