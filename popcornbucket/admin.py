from django.contrib import admin
from popcornbucket.models import Genre, Film, Review, Cinema

# Register your models here.
admin.site.register(Genre)
admin.site.register(Film)
admin.site.register(Review)
admin.site.register(Cinema)