from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Post, Category
from django import forms
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'header', 'category', 'content',
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


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Имя")
    last_name = forms.CharField(label = "Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )

    def clean(self):
        cleaned_date = super().clean()
        email = cleaned_date.get('email')
        email_queryset = User.objects.values('email')
        email_list = [email_user['email'] for email_user in email_queryset]

        if email in email_list:
            raise ValidationError({
                "email": "Error: email already exist"
            })
        return cleaned_date