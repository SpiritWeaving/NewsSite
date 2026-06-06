from django.urls import reverse_lazy
from news.forms import RegisterForm
from django.contrib.auth import login
from django.views.generic import CreateView

# Кастомная регистрация с авто-входом
class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('home')  # После регистрации сразу на главную

    # Метод, который автоматически авторизует пользователя после создания аккаунта
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response
#
# # Вход в систему
# class MyLoginView(LoginView):
#     template_name = 'registration/login.html'
#
# # Выход из системы
# class MyLogoutView(LogoutView):
#     next_page = reverse_lazy('login')  # После выхода отправляем на страницу входа