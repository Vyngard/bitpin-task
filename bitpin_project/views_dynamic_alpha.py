from django.db import transaction
from django.db.models import F, ExpressionWrapper, FloatField
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
            if not (0.0 <= value <= 5.0):
                raise ValueError
        except (TypeError, ValueError):
            return Response(
                {'error': 'Rating value must be between 0 and 5.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update or create the rating
        rating, created = Rating.objects.update_or_create(
            user_id=user_id,
            post_id=post_id,
            defaults={'value': value}
        )

        if created:
            Post.objects.filter(id=post_id).update(
                total_ratings=F('total_ratings') + 1
            )

        # Retrieve the updated total ratings
        post = Post.objects.get(id=post_id)
        total_ratings = post.total_ratings

        # Calculate dynamic alpha
        DYNAMIC_ALPHA = 1.0 / total_ratings

        # Update average_rating atomically
        Post.objects.filter(id=post_id).update(
            average_rating=ExpressionWrapper(
                (value * DYNAMIC_ALPHA) + (F('average_rating') * (1.0 - DYNAMIC_ALPHA)),
                output_field=FloatField()
            )
        )

        return Response(
            {'message': 'Rating recorded successfully.'},
            status=status.HTTP_200_OK
        )


