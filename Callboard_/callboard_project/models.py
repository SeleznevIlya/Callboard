from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from embed_video.fields import EmbedVideoField


class VerifiedUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=50,blank=True, null=True, default=None)


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)
    subscriber = models.ManyToManyField(User, through='Subscribers')

    def __str__(self):
        return f'{self.category_name}'


class Subscribers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    header = models.CharField(max_length=255)
    content = RichTextUploadingField()
    datetime = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True)
    video = EmbedVideoField(blank=True)

    def __str__(self):
        return f'{self.header}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    confirmation = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.post} to {self.author}'



