import os
import requests
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError

from popcornbucket.models import Film, Genre


class Command(BaseCommand):
    help = "Import one movie from TMDb by title"

    def add_arguments(self, parser):
        parser.add_argument("title", type=str, help="Movie title to search for")

    def handle(self, *args, **options):
        api_key = getattr(settings, "TMDB_API_KEY", None) or os.environ.get("TMDB_API_KEY")
        if not api_key:
            raise CommandError("TMDB_API_KEY is not set.")

        title = options["title"]

        # 1) Search for the movie
        search_url = "https://api.themoviedb.org/3/search/movie"
        search_response = requests.get(
            search_url,
            params={
                "query": title,
                "api_key": api_key,
            },
            timeout=20,
        )
        search_response.raise_for_status()
        results = search_response.json().get("results", [])

        if not results:
            raise CommandError(f"No TMDb results found for '{title}'")

        movie = results[0]
        tmdb_id = movie["id"]

        # 2) Get full movie details
        details_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}"
        details_response = requests.get(
            details_url,
            params={"api_key": api_key},
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

        film, created = Film.objects.get_or_create(
            tmdb_id=tmdb_id,
            defaults={
                "title": data.get("title", ""),
                "genre": genre,
                "description": data.get("overview", ""),
                "release_year": release_year,
            },
        )

        if not created:
            film.title = data.get("title", film.title)
            film.genre = genre
            film.description = data.get("overview", film.description)
            if release_year is not None:
                film.release_year = release_year

        # 3) Download the poster into ImageField
        poster_path = data.get("poster_path")
        if poster_path:
            poster_download_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
            poster_response = requests.get(poster_download_url, timeout=20)
            poster_response.raise_for_status()
            filename = f"{tmdb_id}.jpg"
            film.poster.save(filename, ContentFile(poster_response.content), save=False)

        film.save()

        action = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"{action}: {film.title}"))