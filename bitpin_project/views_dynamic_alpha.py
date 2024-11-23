from decimal import Decimal
from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Post, Rating
from .serializers import RatingSerializer

class RatingCreateUpdateViewDynamicAlpha(generics.CreateAPIView):
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

        # Get the rating object if it exists
        try:
            rating = Rating.objects.get(user_id=user_id, post=post)
            rating.value = value
            rating.save()
            total_ratings = post.total_ratings
        except Rating.DoesNotExist:
            post.total_ratings += 1
            total_ratings = post.total_ratings

            # If this is the first rating, set average_rating directly
            if total_ratings == 1:
                post.average_rating = Decimal(value)
                post.save(update_fields=['total_ratings', 'average_rating'])
                return Response({'message': 'Rating recorded successfully.'}, status=status.HTTP_200_OK)

        # Calculate dynamic ALPHA
        DYNAMIC_ALPHA = Decimal('1') / Decimal(total_ratings)

        # Update average_rating using EMA with dynamic ALPHA
        average_rating_old = Decimal(post.average_rating)
        average_rating_new = (Decimal(value) * DYNAMIC_ALPHA) + (average_rating_old * (Decimal('1') - DYNAMIC_ALPHA))

        # Update the post's average_rating
        post.average_rating = average_rating_new
        post.save(update_fields=['average_rating'])

        return Response({'message': 'Rating recorded successfully.'}, status=status.HTTP_200_OK)


