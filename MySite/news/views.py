# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .forms import NewsForm, SubscriptionForm
from .models import News, Category
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .utils import MyMixin, MetaTagsMixin

from django.core.paginator import Paginator

#Тестовая функция для проверки пагинации
def test(request):
    objects = ['Бина', 'Тотошка', 'Вася', 'Динка', 'Стеша', 'Наташа', 'Куруш', 'Оришка']
    paginator = Paginator(objects, 3)
    # Получаем номер страницы из GET-запроса, по умолчанию - 1
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)
    return render(request, "news/test.html", {'page_obj': page_objects})

#Работа с новостями
class HomeNews(MyMixin, MetaTagsMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    #extra_context = {'title' : 'Главная'}
    paginate_by = 3
    mixin_prop = 'The quick brown fox jumps over the lazy dog'
    #Мета-теги
    meta_description = ""
    meta_keywords = ""
    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')

    def get_context_data(self, *, object_list = ..., **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper('Главная')
        context['mixin_prop'] = self.get_prop()
        return context

class NewsByCategory(MyMixin, MetaTagsMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = True
    paginate_by = 3

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'],
                                   is_published=True).select_related('category')

    def get_context_data(self, *, object_list=..., **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper(Category.objects.get(pk = self.kwargs['category_id']))
        return context

class ViewNews(DetailView):
    model = News
    context_object_name = 'news_item'

class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    success_url = reverse_lazy('home')
    login_url = 'login'
    # raise_exception = True

    def form_valid(self, form):
        # Автоматическая привязка текущего залогиненного пользователя к объекту
        form.instance.user = self.request.user
        # Передаем управление базовому классу для сохранения и перенаправления
        return super().form_valid(form)

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

