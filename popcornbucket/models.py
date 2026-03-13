from django.db import models
from django.contrib.auth.models import User
import datetime
from django.db import models
# Create your models here.


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Film(models.Model):
    title = models.CharField(max_length=255)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    description = models.TextField()
    poster_url = models.URLField()
    release_year = models.IntegerField()
    film_id = models.IntegerField()

    def __str__(self):
        return self.title