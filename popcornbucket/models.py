from django.db import models
from django.contrib.auth.models import User
import datetime
<<<<<<< HEAD
=======
from django.db import models
# Create your models here.

>>>>>>> user/simi

class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

<<<<<<< HEAD
class Film(models.Model):
    title = models.CharField(max_length=255)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    description = models.TextField()
    poster_url = models.URLField()
    release_year = models.IntegerField()
    #film_id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    TEXT_MAX_LENGTH = 4000; 

    #review_id = models.AutoField(primary_key=True, unique=True)
    rating = models.IntegerField(default=1)
    review_text = models.CharField(max_length= TEXT_MAX_LENGTH)
    created_at = models.DateTimeField(default=datetime.datetime.now())

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    film_id = models.ForeignKey(Film, on_delete=models.CASCADE)

=======

class Film(models.Model):
    tmdb_id = models.IntegerField(unique=True, null=True, blank=True)
    title = models.CharField(max_length=255)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    description = models.TextField()
    poster = models.ImageField(upload_to='film_posters/', blank=True, null=True)
    release_year = models.IntegerField(null=True, blank=True)
    film_id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.title
>>>>>>> user/simi
