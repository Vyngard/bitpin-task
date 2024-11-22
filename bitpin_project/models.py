from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    total_ratings = models.PositiveIntegerField(default=0)
    average_rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.title


class Rating(models.Model):
    user_id = models.CharField(max_length=255)
    post = models.ForeignKey(Post, related_name='ratings', on_delete=models.CASCADE)
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_id', 'post')

    def __str__(self):
        return f"Rating by {self.user_id} for {self.post.title}"
