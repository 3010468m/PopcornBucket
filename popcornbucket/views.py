from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.db.models import F
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from .models import Film, Genre, Review, Watchlist, Friendship, UserProfile
from .forms import ReviewForm, EditProfileForm


# Create your views here.
# This view is responsible for creating a base/main page
def homepage(request):
    films = Film.objects.filter(cinemas__isnull=False).distinct()[:5]

    return render(request, "popcornbucket/homepage.html", {
        "films": films
    })

def film_list(request):
    films = Film.objects.all()
    genres = Genre.objects.all()

    sort = request.GET.get('sort')
    genre_id = request.GET.get('genre')
    query = request.GET.get('q')

    if query:
        films = films.filter(title__icontains=query)
    
    if genre_id:
        films = films.filter(genre_id=genre_id)

    if sort == 'newest':
        films = films.order_by('-release_year')
    elif sort == 'oldest':
        films = films.order_by('release_year')

    context = {
        'films': films,
        'genres': genres,
        'query':query,
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

def vote_review(request, review_id):
    if request.method == "POST":
        review = get_object_or_404(Review, id=review_id)
        data = json.loads(request.body)
        vote_type = data.get("vote_type")

        if vote_type == "up":
            review.up_votes += 1
        elif vote_type == "down":
            review.down_votes += 1

        review.save()

        return JsonResponse({
            "up_votes": review.up_votes,
            "down_votes": review.down_votes
        })
    
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


@login_required
def add_friend(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    if other_user != request.user:
        Friendship.objects.get_or_create(user=request.user, friend=other_user)
        Friendship.objects.get_or_create(user=other_user, friend=request.user)

    return redirect('user_profile', user_id=other_user.pk)


@login_required
def remove_friend(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    Friendship.objects.filter(user=request.user, friend=other_user).delete()
    Friendship.objects.filter(user=other_user, friend=request.user).delete()

    return redirect('user_profile', user_id=other_user.pk)

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
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    watchlist, created = Watchlist.objects.get_or_create(user=request.user)
    films = watchlist.films.all()
    friends = User.objects.filter(friends_of__user=request.user)
    reviews = Review.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "popcornbucket/profile.html", {
        "user": request.user,
        "films": films,
        "friends":friends,
        "profile": profile,
        "reviews":reviews,
    })

@login_required
def user_profile(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    profile, created = UserProfile.objects.get_or_create(user=profile_user)
    watchlist, created = Watchlist.objects.get_or_create(user=profile_user)
    films = watchlist.films.all()

    reviews = Review.objects.filter(user=profile_user).order_by('-created_at')

    is_friend = Friendship.objects.filter(user=request.user, friend=profile_user).exists()

    return render(request, "popcornbucket/user_profile.html", {
        "profile_user": profile_user,
        "profile":profile,
        "films": films,
        "reviews": reviews,
        "is_friend": is_friend,
    })

@login_required
def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=profile)

    return render(request, 'popcornbucket/edit_profile.html', {'form': form})