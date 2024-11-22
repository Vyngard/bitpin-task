from rest_framework import serializers
from .models import Post, Rating

class PostSerializer(serializers.ModelSerializer):
    user_rating = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'total_ratings', 'average_rating', 'user_rating']

    def get_user_rating(self, obj):
        user_id = self.context['request'].query_params.get('user_id')
        if user_id:
            rating = obj.ratings.filter(user_id=user_id).first()
            return rating.value if rating else None
        return None


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'user_id', 'post', 'value']
