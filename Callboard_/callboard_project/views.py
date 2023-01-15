from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from datetime import datetime
from .forms import PostForm
from .models import Post


class PostList(ListView):
    model = Post
    ordering = '-datetime'
    template_name = 'posts.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'

    def form_valid(self, form):
        author_of_post = form.save(commit=False)
        author_of_post.author = self.request.user
        return super().form_valid(form)


# def get_username_profile(request):
#     #return render_to_response('templates/post.html', {'username': request.user.username})
#     return render(request, 'templates/post.html', {'username': request.user.username})


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_update.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['author_of_post'] = User.objects.get(pk=Post.objects.get(pk=self.request.path[-1]).author_id).username
    #     print(context['author_of_post'])
    #     return context


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
