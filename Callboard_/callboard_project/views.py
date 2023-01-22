import os
import random
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from datetime import datetime
from .forms import PostForm, BaseRegisterForm, MyActivationCodeForm, ReplyForm
from .models import Post, VerifiedUser, Reply


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
    form_class = ReplyForm

    def get_context_data(self, **kwargs):
        data = super(PostDetail,self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            data['comment_form'] = ReplyForm(instance=self.request.user)
        return data

    def post(self, request, *args, **kwargs):
        new_reply = Reply(
            content=request.POST.get('content'),
            author=request.user,
            post=self.get_object()
        )
        new_reply.save()
        author_of_post = Post.objects.get(id=kwargs['pk']).author
        send_mail(
            subject='New Reply',
            message='You have new reply',
            from_email=os.getenv('EMAIL_GOOGLE_FULL'),
            recipient_list=[author_of_post.email]
        )
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'

    def form_valid(self, form):
        author_of_post = form.save(commit=False)
        author_of_post.author = self.request.user
        return super().form_valid(form)


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
    
    
class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = 'confirmation/'


def generate_code():
    random.seed()
    return str(random.randint(10000,99999))


def register(request):
    if not request.user.is_authenticated:
        if request.POST:
            form = BaseRegisterForm(request.POST or None)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                print(username, email)
                my_password1 = form.cleaned_data.get('password1')
                u_f = User.objects.get(username=username, email=email, is_active=False)
                code = generate_code()
                if VerifiedUser.objects.filter(code=code):
                    code = generate_code()
                message = code
                user = authenticate(username=username, password=my_password1)

                VerifiedUser.objects.create(user=u_f, code=code)

                send_mail(subject='код подтверждения',
                          message=message,
                          from_email=os.getenv('EMAIL_GOOGLE_FULL'),
                          recipient_list = [email],
                          fail_silently=False)
                if user and user.is_active:
                    login(request, user)
                    return redirect('/')
                else: #тут добавить редирект на страницу с формой для ввода кода.
                    form.add_error(None, 'Аккаунт не активирован')
                    return redirect('confirmation/')
                    # return render(request, 'registration/register.html', {'form': form})

            else:
                return render(request, 'sign/signup.html', {'form': form})
        else:
            return render(request, 'sign/signup.html', {'form': BaseRegisterForm()})
    else:
        return redirect('/')


def endreg(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            form = MyActivationCodeForm(request.POST)
            if form.is_valid():
                code_use = form.cleaned_data.get("code")
                if VerifiedUser.objects.filter(code=code_use):
                    verified_user = VerifiedUser.objects.get(code=code_use)
                else:
                    form.add_error(None, "Код подтверждения не совпадает.")
                    return render(request, 'sign/otp_comfirmation.html', {'form': form})
                if verified_user.user.is_active == False:
                    verified_user.user.is_active = True
                    verified_user.user.save()
                    # user = authenticate(username=profile.user.username, password=profile.user.password)
                    login(request, verified_user.user)
                    verified_user.delete()
                    return redirect('/')
                else:
                    form.add_error(None, '1Unknown or disabled account')
                    return render(request, 'sign/otp_comfirmation.html', {'form': form})
            else:
                return render(request, 'sign/otp_comfirmation.html', {'form': form})
        else:
            form = MyActivationCodeForm()
            return render(request, 'sign/otp_comfirmation.html', {'form': form})

