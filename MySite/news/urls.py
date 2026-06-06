from django.urls import path
from .views import*

urlpatterns = [
     path('', HomeNews.as_view(), name='home'),
     path('category/<int:category_id>/', NewsByCategory.as_view(extra_context={'title':'Сортировка по категории'}),
           name='category'),
     path('news/<slug:slug>/', ViewNews.as_view(), name='view_news'),
     path('redirect_test', redirect_test, name="redirect_test"),
     path('add_news', CreateNews.as_view(), name="add_news"),
     path('test/', test, name='test')
]
