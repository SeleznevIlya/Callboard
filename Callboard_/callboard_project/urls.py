from django.urls import path, include

from .views import PostList, PostDetail, PostCreate

urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', PostDetail.as_view()),
    path('create/', PostCreate.as_view())

]




