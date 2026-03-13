from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Film, Genre
# Create your views here.

def film_list(request):
    films = Film.objects.all()
    genres = Genre.objects.all()

    sort = request.GET.get('sort')
    genre_id = request.GET.get('genre')

    if genre_id:
        films = films.filter(genre_id=genre_id)

    if sort == 'newest':
        films = films.order_by('-release_year')
    elif sort == 'oldest':
        films = films.order_by('release_year')

    context = {
        'films': films,
        'genres': genres,
    }
    return render(request, 'popcornbucket/film_list.html', context)


def film_detail(request, film_id):
    film = get_object_or_404(Film, id=film_id)
    return render(request, 'popcornbucket/film_detail.html', {'film': film})