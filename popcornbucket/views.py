from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.db.models import F

from .models import Film, Genre, Review, Watchlist
from .forms import ReviewForm


# Create your views here.
# This view is responsible for creating a base/main page
def homepage(request):
    watchlist_films = []

    if request.user.is_authenticated:
        watchlist, created = Watchlist.objects.get_or_create(user=request.user)
        watchlist_films = watchlist.films.all()[:4]

    return render(request, "popcornbucket/homepage.html", {
        "watchlist_films": watchlist_films
    })

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


def film_detail(request, id):
    film = get_object_or_404(Film, id=id)
    context_dict = {}

    try:
        # retrieve all associated reviews
        reviews = Review.objects.filter(film=film)
        sort = request.GET.get('sort')

        if sort == 'newest':
            reviews = reviews.order_by('-created_at')
        elif sort == 'oldest':
            reviews = reviews.order_by('created_at')
        elif sort == 'most_popular':
            reviews = reviews.annotate(total_votes=F('up_votes') -F('down_votes')).order_by('-total_votes')
        in_watchlist = False
        if request.user.is_authenticated:
            watchlist, created = Watchlist.objects.get_or_create(user=request.user)
            in_watchlist = watchlist.films.filter(id=film.pk).exists()

        context_dict['reviews'] = reviews
        context_dict['film'] = film
        context_dict['in_watchlist'] = in_watchlist
    except Film.DoesNotExist:
        context_dict['reviews'] = None
        context_dict['film'] = None
        context_dict['in_watchlist'] = False
    return render(request, 'popcornbucket/film_detail.html', context=context_dict)
    
@login_required
def add_to_watchlist(request, film_id):
    film = get_object_or_404(Film, id=film_id)
    watchlist, created = Watchlist.objects.get_or_create(user=request.user)
    watchlist.films.add(film)
    return redirect('film_detail', id=film_id)


@login_required
def remove_from_watchlist(request, film_id):
    film = get_object_or_404(Film, id=film_id)
    watchlist, created = Watchlist.objects.get_or_create(user=request.user)
    watchlist.films.remove(film)
    return redirect('film_detail', id=film_id)

#@login_required
def write_review(request, film_id):

    # check movie and user are valid (since they're foreign keys)
    film = Film.objects.get(id=film_id)
    user = request.user
    if film is None or user is None :
        return redirect('popcornbucket/homepage.html')

    form = ReviewForm(request.POST)
    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.film = film
            review.user = user
            review.rating = request.POST.get('rating')
            review.save()
            return redirect('film_detail', film_id)
                
        else:
            form = ReviewForm()
            print(form.errors)       


    context_dict = {'form': form, 'film': film}
    return render(request, 'popcornbucket/write_review.html', context=context_dict)

# Sign up
def signup_view(request):
    if request.method == 'POST':
        form= UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect("homepage")
    else:
        form= UserCreationForm()
    return render(request,"popcornbucket/signup.html", {"form": form})


# Login/Logout functions
def login_view(request):
    if request.method == 'POST':
        username=request.POST.get("username")
        password = request.POST.get("password")
        user=authenticate(request,username=username, password=password)
        if user:
            login(request,user)
            return redirect("homepage")
        return render(request, "popcornbucket/login.html", {"error": "Invalid username or password"})
    return render(request, "popcornbucket/login.html")

def logout_view(request):
    logout(request)
    return redirect("homepage")

# User profile 
@login_required
def profile(request):
    watchlist, created = Watchlist.objects.get_or_create(user=request.user)
    films = watchlist.films.all()

    return render(request, "popcornbucket/profile.html", {
        "user": request.user,
        "films": films
    })