from django.contrib import admin
from django.urls import path

from bitpin_project.views import PostListView, RatingCreateUpdateView

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('rate/', RatingCreateUpdateView.as_view(), name='rate-post'),
]
