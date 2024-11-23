from rest_framework import generics, status
from rest_framework.response import Response
from django.db import transaction
from .models import Post, Rating
from .serializers import RatingSerializer
class RatingCreateUpdateViewSimpleAverage(generics.CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        post_id = request.data.get('post')
        value = request.data.get('value')

        try:
            value = float(value)
            if not (0 <= value <= 5):
                raise ValueError
        except (TypeError, ValueError):
            return Response({'error': 'Rating value must be a number between 0 and 5.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Unexpected error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            rating = Rating.objects.get(user_id=user_id, post_id=post_id)
            old_value = rating.value
            rating.value = value
            rating.save()
            total_ratings = post.total_ratings
            total_value = (post.average_rating * total_ratings) - old_value + value
            post.average_rating = total_value / total_ratings
            post.save(update_fields=['average_rating'])
        except Rating.DoesNotExist:
            post.total_ratings += 1
            total_ratings = post.total_ratings
            total_value = (post.average_rating * (total_ratings - 1)) + value
            post.average_rating = total_value / total_ratings
            post.save(update_fields=['total_ratings', 'average_rating'])

        return Response({'message': 'Rating recorded successfully.'}, status=status.HTTP_200_OK)
