from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from transliterate import translit
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    avatar = models.ImageField(upload_to="avatars/", blank=True, verbose_name="Аватар")

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True,
                             verbose_name="Наименование категории")
    description = models.TextField(blank=True, verbose_name="Описание категории")
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['title']

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id':self.pk})

class News(models.Model):
    title = models.CharField(max_length=150, verbose_name="Наименование")
    slug = models.SlugField(max_length=250, unique=True, blank=True)  # Поле для хранения слаг-строки
    content = models.TextField(blank=True, verbose_name="Контент")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    photo = models.ImageField(blank=True, upload_to='photos/%Y/%m/%d', verbose_name="Фото")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, related_name="news")
    author = models.CharField(max_length=50, blank=True, verbose_name="Автор")
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True,
                             verbose_name="Пользователь", related_name="news")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('view_news', kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(translit(self.title, "ru", reversed=True))
        super().save(*args, **kwargs)