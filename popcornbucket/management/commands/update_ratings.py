from django.core.management.base import BaseCommand
from popcornbucket.models import Film
from decimal import Decimal
import requests
import os
import time


class Command(BaseCommand):
    help = "Fetch and update IMDb ratings for films"

    def handle(self, *args, **kwargs):
        OMDB_API_KEY = os.environ.get("OMDB_API_KEY")

        if not OMDB_API_KEY:
            self.stdout.write(self.style.ERROR("OMDB_API_KEY not set"))
            return

        for film in Film.objects.all():
            if film.imdb_id and not film.imdb_rating:
                res = requests.get(
                    "http://www.omdbapi.com/",
                    params={"apikey": OMDB_API_KEY, "i": film.imdb_id},
                    timeout=10
                ).json()

                rating = res.get("imdbRating")

                if rating and rating != "N/A":
                    film.imdb_rating = Decimal(rating)
                    film.save()
                    self.stdout.write(
                        self.style.SUCCESS(f"Updated {film.title}: {rating}")
                    )

                time.sleep(1)  # avoid rate limits