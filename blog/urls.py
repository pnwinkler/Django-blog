from django.urls import path
from .views import (
    PostListView,
    LatestPostsView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    # pk is primary key of post we want to view
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('latest-posts/', LatestPostsView.as_view(), name='latest-posts'),
    path('announcements/', views.announcements, name='announcements'),
    path('about/', views.about, name='blog-about'),
]
