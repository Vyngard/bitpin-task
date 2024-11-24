from django.db.models import F, ExpressionWrapper, FloatField
from rest_framework import generics, status
from rest_framework.response import Response
from django.db import transaction
from .models import Post, Rating
from .serializers import PostSerializer, RatingSerializer

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
            if not (0.0 <= value <= 5.0):
                raise ValueError
        except (TypeError, ValueError):
            return Response({'error': 'Rating value must be between 0 and 5.'},
                            status=status.HTTP_400_BAD_REQUEST)

        ALPHA = 0.1  # Use float instead of Decimal

        # Update or create the rating atomically
        rating, created = Rating.objects.update_or_create(
            user_id=user_id,
            post_id=post_id,
            defaults={'value': value}
        )

        if created:
            Post.objects.filter(id=post_id).update(
                total_ratings=F('total_ratings') + 1
            )

        # Update average rating atomically
        Post.objects.filter(id=post_id).update(
            average_rating=ExpressionWrapper(
                (value * ALPHA) + (F('average_rating') * (1 - ALPHA)),
                output_field=FloatField()
            )
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

        # Reset the posts fields
        post.total_ratings = 0
        post.average_rating = 0.0
        post.save(update_fields=['total_ratings', 'average_rating'])

        # Delete all ratings associated with this post
        Rating.objects.filter(post_id=post_id).delete()

        return Response({'message': 'Post and associated ratings have been reset successfully.'},
                        status=status.HTTP_200_OK)