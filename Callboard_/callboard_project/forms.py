from .models import Post, Category
from django import forms
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'header', 'category', 'content', 'author'
        ]

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        if category is None:
            raise ValidationError({
                "category": "Категория не может быть пустой"
            })
        header = cleaned_data.get('header')
        if header is None:
            raise ValidationError({
                "header": "Error: пустой заголовок"
            })
        content = cleaned_data.get('content')
        if content is None:
            raise ValidationError({
                "content": "Error: пустой текст"
            })
        return cleaned_data
