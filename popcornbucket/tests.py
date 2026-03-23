from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
import json

from popcornbucket.models import (
    Genre, Film, Review, Watchlist, Friendship, UserProfile
)


class ModelTests(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name="Sci-Fi")
        self.user = User.objects.create_user(username="alice", password="testpass123")
        self.film = Film.objects.create(
            title="Inception",
            genre=self.genre,
            description="Dream-sharing thriller",
            release_year=2010,
        )

    def test_film_str(self):
        self.assertEqual(str(self.film), "Inception")

    def test_avg_rating(self):
        Review.objects.create(user=self.user, film=self.film, rating=8, review_text="Good")
        bob = User.objects.create_user(username="bob", password="testpass123")
        Review.objects.create(user=bob, film=self.film, rating=10, review_text="Great")
        self.assertEqual(self.film.avg_rating(), 9)

    def test_user_profile_created(self):
        self.assertTrue(UserProfile.objects.filter(user=self.user).exists())


class ViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="testpass123")
        self.genre = Genre.objects.create(name="Sci-Fi")

        self.film = Film.objects.create(
            title="Inception",
            genre=self.genre,
            description="Test",
            release_year=2010,
        )

        self.review = Review.objects.create(
            user=self.user,
            film=self.film,
            rating=9,
            review_text="Excellent film"
        )

    def test_homepage(self):
        response = self.client.get(reverse("homepage"))
        self.assertEqual(response.status_code, 200)

    def test_film_list(self):
        response = self.client.get(reverse("film_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Inception")

    def test_film_detail(self):
        response = self.client.get(reverse("film_detail", args=[self.film.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Inception")
        self.assertContains(response, "Excellent film")

    def test_invalid_film_detail_returns_404(self):
        response = self.client.get(reverse("film_detail", args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_signup_page_loads(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)

    def test_login_page_loads(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_user_profile_requires_login(self):
        response = self.client.get(reverse("user_profile", args=[self.user.pk]))
        self.assertEqual(response.status_code, 302)

    def test_user_profile_logged_in(self):
        self.client.login(username="alice", password="testpass123")
        response = self.client.get(reverse("user_profile", args=[self.user.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "alice")


class ActionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="testpass123")
        self.other_user = User.objects.create_user(username="bob", password="testpass123")

        self.genre = Genre.objects.create(name="Sci-Fi")
        self.film = Film.objects.create(
            title="Inception",
            genre=self.genre,
            description="Test",
            release_year=2010,
        )

    def test_login(self):
        response = self.client.post(
            reverse("login"),
            {"username": "alice", "password": "testpass123"}
        )
        self.assertEqual(response.status_code, 302)

    def test_signup_creates_user(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "charlie",
                "password1": "ComplexPass123!",
                "password2": "ComplexPass123!",
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="charlie").exists())

    def test_add_to_watchlist(self):
        self.client.login(username="alice", password="testpass123")
        response = self.client.get(reverse("add_to_watchlist", args=[self.film.pk]))
        self.assertEqual(response.status_code, 302)

        watchlist = Watchlist.objects.get(user=self.user)
        self.assertIn(self.film, watchlist.films.all())

    def test_remove_from_watchlist(self):
        watchlist, _ = Watchlist.objects.get_or_create(user=self.user)
        watchlist.films.add(self.film)

        self.client.login(username="alice", password="testpass123")
        response = self.client.get(reverse("remove_from_watchlist", args=[self.film.pk]))
        self.assertEqual(response.status_code, 302)

        watchlist.refresh_from_db()
        self.assertNotIn(self.film, watchlist.films.all())

    def test_add_friend(self):
        self.client.login(username="alice", password="testpass123")
        response = self.client.get(reverse("add_friend", args=[self.other_user.pk]))
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Friendship.objects.filter(user=self.user, friend=self.other_user).exists()
        )
        self.assertTrue(
            Friendship.objects.filter(user=self.other_user, friend=self.user).exists()
        )

    def test_remove_friend(self):
        Friendship.objects.create(user=self.user, friend=self.other_user)
        Friendship.objects.create(user=self.other_user, friend=self.user)

        self.client.login(username="alice", password="testpass123")
        response = self.client.get(reverse("remove_friend", args=[self.other_user.pk]))
        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Friendship.objects.filter(user=self.user, friend=self.other_user).exists()
        )
        self.assertFalse(
            Friendship.objects.filter(user=self.other_user, friend=self.user).exists()
        )

    def test_vote_review(self):
        review = Review.objects.create(
            user=self.user,
            film=self.film,
            rating=9,
            review_text="Test"
        )

        self.client.login(username="alice", password="testpass123")

        response = self.client.post(
            reverse("vote_review", args=[review.pk]),
            data=json.dumps({"vote_type": "up"}),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        review.refresh_from_db()
        self.assertEqual(review.up_votes, 1)

    def test_write_review_post(self):
        self.client.login(username="alice", password="testpass123")

        response = self.client.post(
            reverse("write_review", args=[self.film.pk]),
            {
                "rating": 8,
                "review_text": "Nice review"
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Review.objects.filter(
                user=self.user,
                film=self.film,
                review_text="Nice review"
            ).exists()
        )