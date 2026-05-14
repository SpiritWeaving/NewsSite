# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .forms import NewsForm, SubscriptionForm
from django.http import HttpResponse, HttpResponseRedirect
from .models import News, Category
from django.views.generic import ListView

def index(request):
    news = News.objects.order_by('-created_at')
    context={
        'news': news,
        'title': 'Список новостей',
    }
    return render(request, 'news/index.html', context)

def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    category = Category.objects.get(pk=category_id)
    return render(request, 'news/category.html', {'news':news,
                                                  'category':category})

def jam(request):
    result = '<h1 style="font: Arial">Milky Way, Sun, Moon<h1>'
    return HttpResponse(result + '<h1 style="color: red">Jamushka<h1>')

def view_news(request, news_id):
    news_item = get_object_or_404(News, pk=news_id)
    return render(request,
                  'news/view_news.html',
                  {"news_item": news_item})

def redirect_test(request):
    if request.method == "POST":
        form = SubscriptionForm(request.POST) # Наполняем форму данными из POST
        if form.is_valid():
            # Данные корректны, можно что-то сделать (например, form.cleaned_data)
            return redirect(reverse('category', kwargs={'category_id': 3}))
    else:
        form = SubscriptionForm() # Создаем пустую форму для первого отображения (GET)

    return render(request, 'news/redirect_test.html', {'form': form})

def add_news(request):
    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            #news = News.objects.create(**form.cleaned_data)
            #news.save()
            news = form.save()
            return redirect(news)
    else:
        form = NewsForm()
    return render(request, 'news/add_news.html', {"form": form})