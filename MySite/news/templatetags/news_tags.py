from django import template
from django.shortcuts import reverse
from news.models import Category, News

register = template.Library()

@register.simple_tag(name='get_list_categories' )
def get_categories():
    return Category.objects.all()

@register.simple_tag(name='get_category_amount')
def get_category_amount(category):
    return category.news.count()

@register.inclusion_tag('news/list_categories.html')
def show_categories(arg1="Последние", arg2="Новости"):
    latest_three = list(News.objects.all())[:5]
    categories = []
    for item in latest_three:
        categories.append(item.category)
    # categories = Category.objects.all()
    return {'categories' : categories, 'arg1': arg1, 'arg2':arg2}

@register.inclusion_tag('news/breadcrumb.html')
def show_breadcrumbs(object=None):
    #obj может быть либо объектом Category, либо объектом News
    breadcrumbs = []
    if object:
        breadcrumbs.append({'title' : 'Главная', 'url' : reverse('home')})
        # Если передана новость
        if hasattr(object, 'category'):
            # Добавляем категорию (родителя)
            if object.category:
                breadcrumbs.append({'title': object.category.title, 'url': object.category.get_absolute_url()})
            # Добавляем саму новость (текущий элемент)
            breadcrumbs.append({'title': object.title, 'url': object.get_absolute_url()})

            # Если передана Категория
        else:
            breadcrumbs.append({'title': object.title, 'url': object.get_absolute_url()})

    return {'breadcrumbs': breadcrumbs}
