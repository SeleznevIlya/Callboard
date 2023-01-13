from django.urls import path, include

from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view()),
    path('<int:pk>/update/', PostUpdate.as_view()),
    path('<int:pk>/delete/', PostDelete.as_view()),

]




