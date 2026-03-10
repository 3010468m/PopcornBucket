from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
    
class Review(models.Model):
    TEXT_MAX_LENGTH = 4000; 

    review_id = models.IntegerField(unique=True)
    rating = models.IntegerField(default=1)
    review_text = models.CharField(max_length= TEXT_MAX_LENGTH)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    user_id = models.ForeignKey(User.id, on_delete=models.CASCADE)
    movie_id = models.ForeignKey(Movie.id, on_delete=models.CASCADE)


class Movie(models.Model):
