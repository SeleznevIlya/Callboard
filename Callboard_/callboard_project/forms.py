from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Category, Reply
from django import forms
from django.core.exceptions import ValidationError


class ReplyForm(forms.ModelForm):
    content = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Reply'}))

    class Meta:
        model = Reply
        fields = ['content']


class PostForm(forms.ModelForm):
    video = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'form-control py-4',
            'placeholder': 'Enter video link',

        }), required=False)

    class Meta:
        model = Post
        fields = [
            'header', 'category', 'content', 'image', 'video'
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
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

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


class MyActivationCodeForm(forms.Form):
    error_css_class = 'has-error'
    error_messages = {'password_incorrect':
                          ("Старый пароль не верный. Попробуйте еще раз."),
                      'password_mismatch':
                          ("Пароли не совпадают."),
                      'cod-no':
                          ("Код не совпадает."),}

    def __init__(self, *args, **kwargs):
        super(MyActivationCodeForm, self).__init__(*args, **kwargs)

    code = forms.CharField(required=True,
                           max_length=50,
                           label='Код подтвержения',
                           widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                           error_messages={'required': 'Введите код!','max_length': 'Максимальное количество символов 50'})

    def save(self, commit=True):
        profile = super(MyActivationCodeForm, self).save(commit=False)
        profile.code = self.cleaned_data['code']

        if commit:
            profile.save()
        return profile
