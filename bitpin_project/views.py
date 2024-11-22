from rest_framework import generics, status
from rest_framework.response import Response
from django.db import transaction, models
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

        if not (0 <= float(value) <= 5):
            return Response({'error': 'Rating value must be between 0 and 5.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            rating = Rating.objects.get(user_id=user_id, post_id=post_id)
            old_value = rating.value
            rating.value = value
            rating.save()
            Post.objects.filter(id=post_id).update(
                average_rating=models.F('average_rating') - (old_value - float(value)) / models.F('total_ratings')
            )
        except Rating.DoesNotExist:
            rating = Rating.objects.create(user_id=user_id, post_id=post_id, value=value)
            Post.objects.filter(id=post_id).update(
                total_ratings=models.F('total_ratings') + 1,
                average_rating=(models.F('average_rating') * models.F('total_ratings') + float(value)) / (models.F('total_ratings') + 1)
            )

        return Response({'message': 'Rating recorded successfully.'}, status=status.HTTP_200_OK)
