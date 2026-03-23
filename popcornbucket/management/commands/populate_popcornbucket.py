import os
from decimal import Decimal
from datetime import date

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from django.core.management.base import BaseCommand

from popcornbucket.models import (
    Genre,
    Film,
    Review,
    Cinema,
    Watchlist,
    Friendship,
    UserProfile,
)


class Command(BaseCommand):
    help = "Populate the database with rich sample data for PopcornBucket"

    def handle(self, *args, **options):
        self.stdout.write("Starting population...")

        films_data = [
            {
                "tmdb_id": 27205,
                "title": "Inception",
                "genre": "Sci-Fi",
                "description": "A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea.",
                "release_year": 2010,
                "imdb_id": "tt1375666",
                "imdb_rating": Decimal("8.8"),
                "poster": "inception.jpg",
            },
            {
                "tmdb_id": 157336,
                "title": "Interstellar",
                "genre": "Sci-Fi",
                "description": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
                "release_year": 2014,
                "imdb_id": "tt0816692",
                "imdb_rating": Decimal("8.7"),
                "poster": "interstellar.jpg",
            },
            {
                "tmdb_id": 603,
                "title": "The Matrix",
                "genre": "Sci-Fi",
                "description": "A hacker discovers that reality is a simulation and joins a rebellion against the machines.",
                "release_year": 1999,
                "imdb_id": "tt0133093",
                "imdb_rating": Decimal("8.7"),
                "poster": "matrix.jpg",
            },
            {
                "tmdb_id": 155,
                "title": "The Dark Knight",
                "genre": "Action",
                "description": "Batman faces the Joker, a criminal mastermind who throws Gotham into chaos.",
                "release_year": 2008,
                "imdb_id": "tt0468569",
                "imdb_rating": Decimal("9.0"),
                "poster": "dark_knight.jpg",
            },
            {
                "tmdb_id": 475557,
                "title": "Joker",
                "genre": "Action",
                "description": "A failed comedian spirals into madness and becomes an infamous figure in Gotham.",
                "release_year": 2019,
                "imdb_id": "tt7286456",
                "imdb_rating": Decimal("8.4"),
                "poster": "joker.jpg",
            },
            {
                "tmdb_id": 76341,
                "title": "Mad Max: Fury Road",
                "genre": "Action",
                "description": "In a post-apocalyptic wasteland, Max teams up with Furiosa in a desperate escape.",
                "release_year": 2015,
                "imdb_id": "tt1392190",
                "imdb_rating": Decimal("8.1"),
                "poster": "mad_max_fury_road.jpg",
            },
            {
                "tmdb_id": 496243,
                "title": "Parasite",
                "genre": "Thriller",
                "description": "A poor family infiltrates the lives of a wealthy household.",
                "release_year": 2019,
                "imdb_id": "tt6751668",
                "imdb_rating": Decimal("8.5"),
                "poster": "parasite.jpg",
            },
            {
                "tmdb_id": 550,
                "title": "Fight Club",
                "genre": "Thriller",
                "description": "An office worker forms an underground fight club with a mysterious soap salesman.",
                "release_year": 1999,
                "imdb_id": "tt0137523",
                "imdb_rating": Decimal("8.8"),
                "poster": "fight_club.jpg",
            },
            {
                "tmdb_id": 807,
                "title": "Se7en",
                "genre": "Thriller",
                "description": "Two detectives hunt a serial killer who stages murders around the seven deadly sins.",
                "release_year": 1995,
                "imdb_id": "tt0114369",
                "imdb_rating": Decimal("8.6"),
                "poster": "se7en.jpg",
            },
            {
                "tmdb_id": 244786,
                "title": "Whiplash",
                "genre": "Drama",
                "description": "A young drummer enrolls at a cut-throat music conservatory.",
                "release_year": 2014,
                "imdb_id": "tt2582802",
                "imdb_rating": Decimal("8.5"),
                "poster": "whiplash.jpg",
            },
            {
                "tmdb_id": 13,
                "title": "Forrest Gump",
                "genre": "Drama",
                "description": "The presidencies of Kennedy and Johnson, the Vietnam War, and more unfold through the perspective of Forrest Gump.",
                "release_year": 1994,
                "imdb_id": "tt0109830",
                "imdb_rating": Decimal("8.8"),
                "poster": "forrest_gump.jpg",
            },
            {
                "tmdb_id": 424,
                "title": "Schindler's List",
                "genre": "Drama",
                "description": "In Nazi-occupied Poland, Oskar Schindler gradually becomes concerned for his Jewish workforce.",
                "release_year": 1993,
                "imdb_id": "tt0108052",
                "imdb_rating": Decimal("9.0"),
                "poster": "schindlers_list.jpg",
            },
            {
                "tmdb_id": 129,
                "title": "Spirited Away",
                "genre": "Animation",
                "description": "A ten-year-old girl wanders into a world ruled by gods, witches, and spirits.",
                "release_year": 2001,
                "imdb_id": "tt0245429",
                "imdb_rating": Decimal("8.6"),
                "poster": "spirited_away.jpg",
            },
            {
                "tmdb_id": 12,
                "title": "Finding Nemo",
                "genre": "Animation",
                "description": "After his son is captured, a timid clownfish sets out on a journey across the ocean.",
                "release_year": 2003,
                "imdb_id": "tt0266543",
                "imdb_rating": Decimal("8.2"),
                "poster": "finding_nemo.jpg",
            },
            {
                "tmdb_id": 10681,
                "title": "WALL-E",
                "genre": "Animation",
                "description": "A lonely waste-collecting robot finds a new purpose when he meets a probe named EVE.",
                "release_year": 2008,
                "imdb_id": "tt0910970",
                "imdb_rating": Decimal("8.4"),
                "poster": "wall_e.jpg",
            },
            {
                "tmdb_id": 862,
                "title": "Toy Story",
                "genre": "Comedy",
                "description": "A cowboy doll is threatened when a new spaceman action figure becomes the favourite toy.",
                "release_year": 1995,
                "imdb_id": "tt0114709",
                "imdb_rating": Decimal("8.3"),
                "poster": "toy_story.jpg",
            },
            {
                "tmdb_id": 105,
                "title": "Back to the Future",
                "genre": "Comedy",
                "description": "A teenager is accidentally sent back in time in a DeLorean built by his eccentric scientist friend.",
                "release_year": 1985,
                "imdb_id": "tt0088763",
                "imdb_rating": Decimal("8.5"),
                "poster": "back_to_the_future.jpg",
            },
            {
                "tmdb_id": 37165,
                "title": "The Truman Show",
                "genre": "Comedy",
                "description": "A man slowly discovers that his entire life is actually a reality television show.",
                "release_year": 1998,
                "imdb_id": "tt0120382",
                "imdb_rating": Decimal("8.2"),
                "poster": "truman_show.jpg",
            },
        ]

        created_films = {}

        for film_data in films_data:
            genre, _ = Genre.objects.get_or_create(name=film_data["genre"])

            film, created = Film.objects.get_or_create(
                title=film_data["title"],
                defaults={
                    "tmdb_id": film_data["tmdb_id"],
                    "genre": genre,
                    "description": film_data["description"],
                    "release_year": film_data["release_year"],
                    "imdb_id": film_data["imdb_id"],
                    "imdb_rating": film_data["imdb_rating"],
                },
            )

            if not created:
                film.tmdb_id = film_data["tmdb_id"]
                film.genre = genre
                film.description = film_data["description"]
                film.release_year = film_data["release_year"]
                film.imdb_id = film_data["imdb_id"]
                film.imdb_rating = film_data["imdb_rating"]

            poster_filename = film_data.get("poster")
            if poster_filename:
                poster_path = os.path.join(settings.MEDIA_ROOT, "film_posters", poster_filename)
                if os.path.exists(poster_path):
                    if film.poster:
                        film.poster.delete(save=False)

                    with open(poster_path, "rb") as f:
                        film.poster.save(poster_filename, File(f), save=False)

            film.save()
            created_films[film.title] = film
            self.stdout.write(self.style.SUCCESS(f"Added film: {film.title}"))

        cinema_data = [
            {
                "name": "ODEON Luxe Glasgow Quay",
                "location": "Springfield Quay, Glasgow",
                "website": "https://www.odeon.co.uk/cinemas/glasgow-quay/",
                "films": ["Inception", "Interstellar", "The Dark Knight", "Parasite", "Whiplash", "WALL-E"],
            },
            {
                "name": "Vue Glasgow St Enoch",
                "location": "St Enoch Centre, Glasgow",
                "website": "https://www.myvue.com/cinema/glasgow-st-enoch/whats-on",
                "films": ["The Matrix", "Joker", "Mad Max: Fury Road", "Finding Nemo", "Toy Story", "Back to the Future"],
            },
            {
                "name": "Vue Glasgow Fort",
                "location": "Glasgow Fort, Glasgow",
                "website": "https://www.myvue.com/cinema/glasgow-fort/whats-on",
                "films": ["Inception", "Fight Club", "Se7en", "Forrest Gump", "The Truman Show", "Toy Story"],
            },
            {
                "name": "Everyman Glasgow",
                "location": "Princes Square, Glasgow",
                "website": "https://www.everymancinema.com/venues-list/x11dq-everyman-glasgow/",
                "films": ["Parasite", "Whiplash", "Schindler's List", "Spirited Away", "The Truman Show", "Joker"],
            },
            {
                "name": "Cineworld Glasgow Silverburn",
                "location": "Silverburn, Glasgow",
                "website": "https://www.cineworld.co.uk/cinemas/glasgow-silverburn/088",
                "films": ["Interstellar", "The Dark Knight", "Mad Max: Fury Road", "WALL-E", "Finding Nemo", "Back to the Future"],
            },
        ]

        for cinema_info in cinema_data:
            cinema, _ = Cinema.objects.get_or_create(
                name=cinema_info["name"],
                defaults={
                    "location": cinema_info["location"],
                    "website": cinema_info["website"],
                },
            )

            cinema.location = cinema_info["location"]
            cinema.website = cinema_info["website"]
            cinema.save()

            for film_title in cinema_info["films"]:
                if film_title in created_films:
                    cinema.films.add(created_films[film_title])

        users_data = [
            {
                "username": "alice",
                "email": "alice@example.com",
                "password": "testpass123",
                "profile_picture": "alice.jpg",
                "date_of_birth": date(1998, 5, 14),
            },
            {
                "username": "bob",
                "email": "bob@example.com",
                "password": "testpass123",
                "profile_picture": "bob.jpg",
                "date_of_birth": date(1995, 11, 2),
            },
            {
                "username": "charlie",
                "email": "charlie@example.com",
                "password": "testpass123",
                "profile_picture": "charlie.jpg",
                "date_of_birth": date(2000, 1, 25),
            },
        ]

        created_users = {}

        for user_data in users_data:
            user, _ = User.objects.get_or_create(
                username=user_data["username"],
                defaults={"email": user_data["email"]},
            )
            user.email = user_data["email"]
            user.set_password(user_data["password"])
            user.save()

            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.date_of_birth = user_data["date_of_birth"]

            profile_picture_filename = user_data.get("profile_picture")
            if profile_picture_filename:
                profile_picture_path = os.path.join(
                    settings.MEDIA_ROOT,
                    "profile_pics",
                    profile_picture_filename,
                )

                if os.path.exists(profile_picture_path):
                    if profile.profile_picture:
                        profile.profile_picture.delete(save=False)

                    with open(profile_picture_path, "rb") as f:
                        profile.profile_picture.save(
                            profile_picture_filename,
                            File(f),
                            save=False,
                        )

            profile.save()
            created_users[user.username] = user

        watchlists = {
            "alice": ["Inception", "Parasite", "Spirited Away"],
            "bob": ["The Dark Knight", "Interstellar", "Whiplash"],
            "charlie": ["The Matrix", "WALL-E", "Back to the Future"],
        }

        for username, film_titles in watchlists.items():
            watchlist, _ = Watchlist.objects.get_or_create(user=created_users[username])
            for title in film_titles:
                watchlist.films.add(created_films[title])

        Friendship.objects.get_or_create(user=created_users["alice"], friend=created_users["bob"])
        Friendship.objects.get_or_create(user=created_users["bob"], friend=created_users["alice"])
        Friendship.objects.get_or_create(user=created_users["alice"], friend=created_users["charlie"])
        Friendship.objects.get_or_create(user=created_users["charlie"], friend=created_users["alice"])

        reviews_data = [
            ("alice", "Inception", 9, "Clever, layered and still one of the most exciting sci-fi films ever."),
            ("bob", "Interstellar", 9, "Huge ideas, emotional storytelling, and a brilliant score."),
            ("charlie", "The Matrix", 10, "Stylish, influential and endlessly rewatchable."),
            ("alice", "The Dark Knight", 10, "A gripping superhero film with an unforgettable villain."),
            ("bob", "Joker", 8, "Dark and unsettling, with a powerful lead performance."),
            ("charlie", "Mad Max: Fury Road", 9, "Relentless energy and incredible action from start to finish."),
            ("alice", "Parasite", 9, "Sharp, tense and full of social commentary."),
            ("bob", "Fight Club", 8, "Bold and provocative, with a memorable twist."),
            ("charlie", "Se7en", 9, "Bleak, intense and brilliantly constructed."),
            ("alice", "Whiplash", 9, "Intense, gripping, and brilliantly acted."),
            ("bob", "Forrest Gump", 8, "Warm, funny and emotional with a classic central performance."),
            ("charlie", "Schindler's List", 10, "Heartbreaking and essential cinema."),
            ("alice", "Spirited Away", 10, "Beautifully animated and full of imagination."),
            ("bob", "Finding Nemo", 8, "Funny, heartfelt and perfect for families."),
            ("charlie", "WALL-E", 9, "Inventive, touching and visually wonderful."),
            ("alice", "Toy Story", 8, "A timeless and charming animation classic."),
            ("bob", "Back to the Future", 9, "Fast, funny and one of the most entertaining films ever made."),
            ("charlie", "The Truman Show", 9, "Smart, funny and surprisingly emotional."),
        ]

        for username, film_title, rating, review_text in reviews_data:
            Review.objects.get_or_create(
                user=created_users[username],
                film=created_films[film_title],
                defaults={
                    "rating": rating,
                    "review_text": review_text,
                },
            )

        self.stdout.write(self.style.SUCCESS("Population complete."))