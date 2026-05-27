# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .forms import NewsForm, SubscriptionForm
from .models import News, Category
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy

class HomeNews(ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    #extra_context = {'title' : 'Главная'}
    paginate_by = 3

    def get_queryset(self):
        return News.objects.filter(is_published=True)

    def get_context_data(self, *, object_list = ..., **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        return context

class NewsByCategory(ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = True

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True)

    def get_context_data(self, *, object_list=..., **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk = self.kwargs['category_id'])
        return context

class ViewNews(DetailView):
    model = News
    context_object_name = 'news_item'

class CreateNews(CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    success_url = reverse_lazy('home')

# def view_news(request, news_id):
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request,
#                   'news/view_news.html',
#                   {"news_item": news_item})

def redirect_test(request):
    if request.method == "POST":
        form = SubscriptionForm(request.POST) # Наполняем форму данными из POST
        if form.is_valid():
            return redirect(reverse('category', kwargs={'category_id': 3}))
    else:
        form = SubscriptionForm() # Создаем пустую форму для первого отображения (GET)

    return render(request, 'news/redirect_test.html', {'form': form})

# def add_news(request):
#     if request.method == "POST":
#         form = NewsForm(request.POST, request.FILES)
#         if form.is_valid():
#             #news = News.objects.create(**form.cleaned_data)
#             #news.save()
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {"form": form})