from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Film(models.Model):
    title = models.CharField(max_length=200)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='films')
    description = models.TextField()
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)
    release_date = models.DateField()

    def __str__(self):
        return self.title