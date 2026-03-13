from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Film, Genre, Review
from .forms import ReviewForm


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
    film = get_object_or_404(Film, film_id=film_id)
    return render(request, 'popcornbucket/film_detail.html', {'film': film})

#@login_required
def write_review(request):
    # check movie and user are valid (since they're foreign keys)
    if film is None or user is None :
        return redirect('/popcornbucket/film_detail.html', {'film': film}) # return to homepage instead?

    film = Film.objects.get(pk=film_id)
    user = request.user
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            if film and user:
                review = form.save(commit=False)
                review.review_text = request.PST['review_text']
                review.rating = int(request.POST['rating'])
                review.save()
                
                return redirect(reverse('popcornbucket:film_detail', kwargs={'filn': film})) # return to movie page
        else:
            print(form.errors)       


    context_dict = {'form': form, 'film': film}
    return render(request, 'popcornbucket/write_review.html', context=context_dict)

def show_reviews(request, film): # incorporated into show_movie
    context_dict = {}

    try:
        # retrieve all associated reviews
        reviews = Review.objects(filter(film=film))
        context_dict['reviews'] = reviews
        context_dict['film'] = film
    except Film.DoesNotExist:
        context_dict['reviews'] = None
        context_dict['film'] = None
    
    return render(request, 'popcornbucket.html', context=context_dict)

