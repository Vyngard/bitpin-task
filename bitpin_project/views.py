from rest_framework import generics, status
from rest_framework.response import Response
from django.db import transaction, models
from .models import Post, Rating
from .serializers import PostSerializer, RatingSerializer
from decimal import Decimal



class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class RatingCreateUpdateView(generics.CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        post_id = request.data.get('post')
        value = request.data.get('value')

        # Validate the rating value
        try:
            value = float(value)
            if not (0 <= value <= 5):
                raise ValueError
        except (TypeError, ValueError):
            return Response({'error': 'Rating value must be between 0 and 5.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Get the post object
        try:
            post = Post.objects.select_for_update().get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        ALPHA = Decimal('0.1')

       # Get the rating object if it exists
        try:
            rating = Rating.objects.get(user_id=user_id, post=post)
            rating.value = value
            rating.save()
            Post.objects.filter(id=post_id).update(
                average_rating=(Decimal(value) * ALPHA) + (models.F('average_rating') * (1 - ALPHA))
            )
        except Rating.DoesNotExist:
            Post.objects.filter(id=post_id).update(
                total_ratings=models.F('total_ratings') + 1,
                average_rating=(Decimal(value) * ALPHA) + (models.F('average_rating') * (1 - ALPHA))
            )

        return Response({'message': 'Rating recorded successfully.'}, status=status.HTTP_200_OK)

class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostResetView(generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        post_id = request.data.get('post')

        if not post_id:
            return Response({'error': 'Post ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        # Reset the post's fields
        post.total_ratings = 0
        post.average_rating = 0
        post.save(update_fields=['total_ratings', 'average_rating'])

        # Delete all ratings associated with this post
        Rating.objects.filter(post_id=post_id).delete()

        return Response({'message': 'Post and associated ratings have been reset successfully.'},
                        status=status.HTTP_200_OK)
