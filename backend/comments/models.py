from django.db import models
from django_mongodb_backend.fields import ObjectIdAutoField

class ScrapedPost(models.Model):
    id = ObjectIdAutoField(primary_key=True)
    url = models.URLField(max_length=500, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url

class Comment(models.Model):
    id = ObjectIdAutoField(primary_key=True)
    post = models.ForeignKey(ScrapedPost, related_name='comments', on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    text = models.TextField()
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.username}: {self.text[:20]}..."
