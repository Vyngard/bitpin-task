from django.urls import path
from .views import PostListView, RatingCreateUpdateView, PostCreateView, PostResetView
from .views_dynamic_alpha import RatingCreateUpdateViewDynamicAlpha
from .views_simple_average import RatingCreateUpdateViewSimpleAverage

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/create/', PostCreateView.as_view(), name='post-create'),
    path('rate/', RatingCreateUpdateView.as_view(), name='rate-post'),
    path('rate_simple/', RatingCreateUpdateViewSimpleAverage.as_view(), name='rate-post-simple'),
    path('reset_post/', PostResetView.as_view(), name='reset_post'),
    path('rate_dynamic/', RatingCreateUpdateViewDynamicAlpha.as_view(), name='rate-post-dynamic'),
]

# TODO: add views_simple_average.py and views_dynamic_alpha.py 