import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'popcornbucket_project.settings')
django.setup()

from popcornbucket.models import Genre, Film


def populate():
    films_data = {
        "Action": [
            {
                "title": "The Dark Knight",
                "description": "Batman faces the Joker in Gotham City.",
                "poster": "https://example.com/dark_knight.jpg",
                "release_year": 2008,
            },
            {
                "title": "Mad Max: Fury Road",
                "description": "A high-speed chase through a post-apocalyptic desert.",
                "poster": "https://example.com/mad_max.jpg",
                "release_year": 2015,
            },
        ],
        "Sci-Fi": [
            {
                "title": "Inception",
                "description": "A thief enters dreams to steal and plant ideas.",
                "poster": "https://example.com/inception.jpg",
                "release_year": 2010,
            },
            {
                "title": "Interstellar",
                "description": "A team travels through a wormhole to save humanity.",
                "poster": "https://example.com/interstellar.jpg",
                "release_year": 2014,
            },
        ],
        "Comedy": [
            {
                "title": "Superbad",
                "description": "Two friends try to enjoy one unforgettable night.",
                "poster": "https://example.com/superbad.jpg",
                "release_year": 2007,
            },
            {
                "title": "The Hangover",
                "description": "Three friends retrace a wild night in Las Vegas.",
                "poster": "https://example.com/hangover.jpg",
                "release_year": 2009,
            },
        ],
        "Drama": [
            {
                "title": "The Shawshank Redemption",
                "description": "A banker forms an unlikely friendship in prison.",
                "poster": "https://example.com/shawshank.jpg",
                "release_year": 1994,
            },
            {
                "title": "The Shawshank Redemptio",
                "description": "A banker forms an unlikely friendship in prison.",
                "poster": "https://example.com/shawshank.jpg",
                "release_year": 1994,
            },
            {
                "title": "The Shawshank Redempti",
                "description": "A banker forms an unlikely friendship in prison.",
                "poster": "https://example.com/shawshank.jpg",
                "release_year": 1994,
            },
            {
                "title": "The Shawshank Redemptio",
                "description": "A banker forms an unlikely friendship in prison.",
                "poster": "https://example.com/shawshank.jpg",
                "release_year": 1994,
            }
        ],
    }

    for genre_name, films in films_data.items():
        genre, created = Genre.objects.get_or_create(name=genre_name)
        if created:
            print(f"Created genre: {genre.name}")
        else:
            print(f"Genre already exists: {genre.name}")

        for film in films:
            obj, created = Film.objects.get_or_create(
                title=film["title"],
                defaults={
                    "genre": genre,
                    "description": film["description"],
                    "poster": film["poster"],
                    "release_year": film["release_year"],
                },
            )

            if created:
                print(f"Added film: {obj.title}")
            else:
                print(f"Film already exists: {obj.title}")


if __name__ == "__main__":
    print("Populating PopcornBucket...")
    populate()
    print("Done.")