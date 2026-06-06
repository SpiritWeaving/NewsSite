from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from news.views import*
from news.forms import LoginForm
from .views import *
from django.contrib.auth import views as auth_views

# Функция редиректа пишется прямо здесь для надежности
def root_redirect(request):
    return redirect('home') # Укажите имя 'name' из Шага 1

# urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(
        template_name= "registration/login.html",
        form_class = LoginForm,
    ), name="login"),
    path('logout/', auth_views.LogoutView.as_view(
        next_page = "home"
    ), name="logout"),
    path('register/', RegisterView.as_view(), name="register"),
    path('news/', include('news.urls'), name='news_view'),
    path("__reload__/", include("django_browser_reload.urls")),
    path('', root_redirect, name='root') # перенаправляет с /
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls')), ]

