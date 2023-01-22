import os
import random
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
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
            data['author_of_post'] = Post.objects.filter(author=self.request.user)
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


class ReplyList(LoginRequiredMixin, ListView):
    model = Reply
    template_name = 'reply_list.html'
    paginate_by = 10
    ordering = 'id'

    def get_queryset(self):
        queryser = super(ReplyList, self).get_queryset()
        post_id = self.kwargs.get('post_id')
        return queryser.filter(post_id=post_id) if post_id else queryser.filter(author=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super(ReplyList, self).get_context_data()
        data['post_replys'] = Post.objects.filter(author=self.request.user)
        return data


class ReplyConfirmed(LoginRequiredMixin, CreateView):
    model = Reply
    template_name = 'reply_confirmed.html'
    form_class = ReplyForm
    context_object_name = 'confirmed'
    success_url = 'replys/'

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        reply_id = self.kwargs.get('pk')
        Reply.objects.filter(pk=reply_id).update(confirmation=True)
        data['message'] = 'This reply was confirmed'
        send_mail(
            subject='Reply comfirmed',
            message=f'User {self.request.user} comfirmed your reply',
            from_email=os.getenv('EMAIL_GOOGLE_FULL'),
            recipient_list=[User.objects.filter(username=self.request.user).values('email')[0]['email']]
        )
        return data


class ReplyUnconfirmed(LoginRequiredMixin, DeleteView):
    model = Reply
    template_name = 'reply_unconfirmed.html'
    success_url = reverse_lazy('reply_list')


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
    return str(random.randint(10000, 99999))


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
                else:
                    form.add_error(None, 'Аккаунт не активирован')
                    return redirect('confirmation/')
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

