from django.urls import path, include

from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete, BaseRegisterView, register, endreg, \
    ReplyList, ReplyConfirmed, ReplyUnconfirmed
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view()),
    path('<int:pk>/update/', PostUpdate.as_view()),
    path('<int:pk>/delete/', PostDelete.as_view()),
    path('replys/', ReplyList.as_view(), name='reply_list'),
    path('replys/<int:post_id>', ReplyList.as_view(), name='reply_post'),
    path('reply_confirmed/<int:pk>', ReplyConfirmed.as_view(), name='reply_confirmed'),
    path('reply_unconfirmed/<int:pk>', ReplyUnconfirmed.as_view(), name='reply_unconfirmed'),
    path('login/',
         LoginView.as_view(template_name='sign/login.html'),
         name='login'),
    path('logout/',
         LogoutView.as_view(template_name='sign/logout.html'),
         name='logout'),
    path('signup/',
         register, name='register'),
    path('signup/confirmation/',
         endreg, name='endreg')
]
