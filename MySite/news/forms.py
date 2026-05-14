from django import forms
from news.models import News, Category
import re
from django.core.exceptions import ValidationError

class NewsForm(forms.ModelForm):
    # title = forms.CharField(max_length=150, label="Название",
    #                         widget=forms.TextInput(attrs={"class":"form-control"}))
    # content = forms.CharField(required=False, label="Текст",
    #                           widget=forms.Textarea(attrs={"class":"form-control",
    #                                                        "rows":5}))
    # is_published = forms.BooleanField(label="Опубликовано?")
    # category = forms.ModelChoiceField(queryset=Category.objects.all(),
    #                                   empty_label="Выберите категорию", label="Категория",
    #                                   widget=forms.Select(attrs={"class":"form-control"}))
    class Meta:
        model = News
        # fields = '__all__'
        fields = ['title', 'content', 'author', 'photo', 'is_published', 'category']
        widgets = {
            'title': forms.TextInput(attrs={"class":"form-control"}),
            'content': forms.Textarea(attrs={"class":"form-control", "rows":5}),
            'category': forms.Select(attrs={"class":"form-control"}),
            'photo': forms.FileInput(attrs={"class":"form-control"}),
            'author': forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError("Название не должно начинаться с цифры.")
        return title

    def clean_author(self):
        author = self.cleaned_data['author']
        if len(author) < 2:
            raise ValidationError("Имя автора слишком короткое")
        return author

class SubscriptionForm(forms.Form):
    email = forms.EmailField(label="Адрес электронной почты",
                             help_text="me@example.ru")
    name = forms.CharField(label="Имя", max_length=100)