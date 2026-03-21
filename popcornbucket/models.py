from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import datetime
from django.db import models
from django.db.models import Avg
# Create your models here.


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
    
class Film(models.Model):
    tmdb_id = models.IntegerField(unique=True, null=True, blank=True)
    title = models.CharField(max_length=255)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    description = models.TextField()
    poster = models.ImageField(upload_to='film_posters/', blank=True, null=True)
    release_year = models.IntegerField(null=True, blank=True)
    
    def avg_rating(self):
        return self.review_set.aggregate(Avg('rating'))['rating__avg']

    def __str__(self):
        return self.title


class Review(models.Model):
    TEXT_MAX_LENGTH = 4000; 

    rating = models.IntegerField(default=0)
    review_text = models.CharField(max_length= TEXT_MAX_LENGTH)
    created_at = models.DateTimeField(default=now)
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)


class Cinema(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255, blank=True)
    website = models.URLField(blank=True)
    films = models.ManyToManyField(Film, blank=True, related_name='cinemas')

    def __str__(self):
        return self.name
    
class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='watchlist')
    films = models.ManyToManyField('Film', blank=True, related_name='in_watchlists')

    def __str__(self):
        return f"{self.user.username}'s watchlist"

class Friendship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends_of')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'friend')

    def __str__(self):
        return f"{self.user.username} -> {self.friend.username}"