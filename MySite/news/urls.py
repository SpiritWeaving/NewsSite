from django.urls import path
from .views import*

urlpatterns = [
     path('', index, name='home'),
     path('category/<int:category_id>/', get_category, name='category'),
     path('view_news/<int:news_id>/', view_news, name='view_news'),
     path('redirect_test', redirect_test, name="redirect_test"),
     path('add_news', add_news, name="add_news")
]
