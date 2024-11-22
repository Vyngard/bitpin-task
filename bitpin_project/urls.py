from django.urls import path
from .views import PostListView, RatingCreateUpdateView, PostCreateView, RatingCreateUpdateViewSimpleAverage, PostResetView

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/create/', PostCreateView.as_view(), name='post-create'),
    path('rate/', RatingCreateUpdateView.as_view(), name='rate-post'),
    path('rate_simple/', RatingCreateUpdateViewSimpleAverage.as_view(), name='rate-post-simple'),
    path('reset_post/', PostResetView.as_view(), name='reset_post'),
]