from django.db import models
from django.urls import reverse
from django.utils.text import slugify

def transliterate_rus(text):
    cyrillic = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'
    }
    text = text.lower()
    # Заменяем русские буквы по словарю, остальные оставляем как есть
    return "".join(cyrillic.get(char, char) for char in text)

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
    slug = models.SlugField(unique=True, default=slugify(transliterate_rus(str(title))))  # Поле для хранения слаг-строки
    content = models.TextField(blank=True, verbose_name="Контент")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    photo = models.ImageField(blank=True, upload_to='photos/%Y/%m/%d', verbose_name="Фото")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    author = models.CharField(max_length=50, blank=True, verbose_name="Автор")

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
            self.slug = slugify(transliterate_rus(self.title))
        super().save(*args, **kwargs)