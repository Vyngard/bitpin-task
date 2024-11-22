from django.urls import path
from .views import PostListView, RatingCreateUpdateView, PostCreateView

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/create/', PostCreateView.as_view(), name='post-create'),
    path('rate/', RatingCreateUpdateView.as_view(), name='rate-post'),
]