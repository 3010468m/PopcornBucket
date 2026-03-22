import os
import requests
from decimal import Decimal, InvalidOperation

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError

from popcornbucket.models import Film, Genre


class Command(BaseCommand):
    help = "Import one movie from TMDb by title"

    def add_arguments(self, parser):
        parser.add_argument("title", type=str, help="Movie title to search for")

    def handle(self, *args, **options):
        tmdb_api_key = getattr(settings, "TMDB_API_KEY", None) or os.environ.get("TMDB_API_KEY")
        omdb_api_key = getattr(settings, "OMDB_API_KEY", None) or os.environ.get("OMDB_API_KEY")

        if not tmdb_api_key:
            raise CommandError("TMDB_API_KEY is not set.")

        title = options["title"]

        # 1) Search for the movie on TMDb
        search_url = "https://api.themoviedb.org/3/search/movie"
        search_response = requests.get(
            search_url,
            params={
                "query": title,
                "api_key": tmdb_api_key,
            },
            timeout=20,
        )
        search_response.raise_for_status()
        results = search_response.json().get("results", [])

        if not results:
            raise CommandError(f"No TMDb results found for '{title}'")

        movie = results[0]
        tmdb_id = movie["id"]

        # 2) Get full movie details from TMDb
        details_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}"
        details_response = requests.get(
            details_url,
            params={"api_key": tmdb_api_key},
            timeout=20,
        )
        details_response.raise_for_status()
        data = details_response.json()

        genre_name = "Unknown"
        if data.get("genres"):
            genre_name = data["genres"][0]["name"]

        genre, _ = Genre.objects.get_or_create(name=genre_name)

        release_year = None
        if data.get("release_date"):
            try:
                release_year = int(data["release_date"][:4])
            except (TypeError, ValueError):
                release_year = None

        # 3) Get IMDb ID from TMDb external IDs
        imdb_id = None
        external_ids_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/external_ids"
        external_ids_response = requests.get(
            external_ids_url,
            params={"api_key": tmdb_api_key},
            timeout=20,
        )
        external_ids_response.raise_for_status()
        external_ids_data = external_ids_response.json()
        imdb_id = external_ids_data.get("imdb_id")

        # 4) Get IMDb rating from OMDb
        imdb_rating = None
        if omdb_api_key and imdb_id:
            omdb_url = "http://www.omdbapi.com/"
            omdb_response = requests.get(
                omdb_url,
                params={
                    "apikey": omdb_api_key,
                    "i": imdb_id,
                },
                timeout=20,
            )
            omdb_response.raise_for_status()
            omdb_data = omdb_response.json()

            raw_rating = omdb_data.get("imdbRating")
            if raw_rating and raw_rating != "N/A":
                try:
                    imdb_rating = Decimal(raw_rating)
                except (InvalidOperation, TypeError):
                    imdb_rating = None

        film, created = Film.objects.get_or_create(
            tmdb_id=tmdb_id,
            defaults={
                "title": data.get("title", ""),
                "genre": genre,
                "description": data.get("overview", ""),
                "release_year": release_year,
                "imdb_id": imdb_id,
                "imdb_rating": imdb_rating,
            },
        )

        if not created:
            film.title = data.get("title", film.title)
            film.genre = genre
            film.description = data.get("overview", film.description)
            film.imdb_id = imdb_id
            film.imdb_rating = imdb_rating

            if release_year is not None:
                film.release_year = release_year

        # 5) Download the poster into ImageField
        poster_path = data.get("poster_path")
        if poster_path:
            poster_download_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
            poster_response = requests.get(poster_download_url, timeout=20)
            poster_response.raise_for_status()
            filename = f"{tmdb_id}.jpg"
            film.poster.save(filename, ContentFile(poster_response.content), save=False)

        film.save()

        action = "Created" if created else "Updated"
        self.stdout.write(
            self.style.SUCCESS(
                f"{action}: {film.title} | IMDb ID: {film.imdb_id} | IMDb rating: {film.imdb_rating}"
            )
        )