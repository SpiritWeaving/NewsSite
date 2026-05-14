from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True,
                             verbose_name="Наименование категории")
    description = models.TextField(blank=True, verbose_name="Описание категории")
    thumbnail = models.ImageField(blank=True, upload_to="categories/", verbose_name="Изображение категории")

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
    content = models.TextField(blank=True, verbose_name="Контент")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    photo = models.ImageField(blank=True, upload_to='photos/%Y/%m/%d', verbose_name="Фото")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    author = models.CharField(max_length=50, verbose_name="Автор", blank=True)

    def __str__(self):
        return self.title

    def just_a_little_trolling(self):
        return "Foxieshka";

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('view_news', kwargs={'news_id':self.pk})
