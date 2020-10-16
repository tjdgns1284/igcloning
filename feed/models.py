from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail

# Create your models here.
class Hashtag(models.Model):
    content = models.TextField()

    def __str__(self):
        return self.content

class Article(models.Model):
    
    image = ProcessedImageField(
        blank=True,
        processors=[Thumbnail(900, 500)],
        format='JPEG',
        options={'quality': 100},
       
    )
    content = models.TextField()
    hashtags = models.ManyToManyField(Hashtag, related_name='tagged_articles', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_articles')

class Comment(models.Model):
    article= models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_comments')