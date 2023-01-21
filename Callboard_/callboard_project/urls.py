from django.urls import path, include

from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete, BaseRegisterView, register, endreg
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view()),
    path('<int:pk>/update/', PostUpdate.as_view()),
    path('<int:pk>/delete/', PostDelete.as_view()),
    path('login/',
         LoginView.as_view(template_name = 'sign/login.html'),
         name='login'),
    path('logout/',
         LogoutView.as_view(template_name = 'sign/logout.html'),
         name='logout'),
    path('signup/',
         register, name='register'),
    path('signup/confirmation/',
         endreg, name='endreg')
]
