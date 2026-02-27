# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from .models import News, Category

def index(request):
    news = News.objects.order_by('-created_at')
    categories = Category.objects.all()
    # result = "<h1>Список новостей</h1>"
    # for item in news:
    #     result += f'<div>\n<h2>{item.title}</h2>\n<p>{item.content}</p>\n</div><hr>\n'
    # return HttpResponse(result)

    context={
        'news': news,
        'title': 'Список новостей',
        'categories': categories,
    }
    return render(request, 'news/index.html', context)

def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    categories = Category.objects.all()
    category = Category.objects.get(pk=category_id)
    return render(request, 'news/category.html', {'news':news, 'categories':categories,
                                                  'category':category})

def jam(request):
    result = '<h1 style="font: Arial">Milky Way, Sun, Moon<h1>'
    return HttpResponse(result + '<h1 style="color: red">Jamushka<h1>')