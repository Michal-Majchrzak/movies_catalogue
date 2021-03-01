import requests
import random

V4_TOKEN = ""


def get_tmdb_response(url: str) -> dict:
    headers = {'Authorization': f"Bearer {V4_TOKEN}"}
    response = requests.get(url, headers=headers)
    return response.json()


def _get_movies_genres():
    url = "https://api.themoviedb.org/3/genre/movie/list"
    genres = get_tmdb_response(url).get('genres')
    result = {}

    for genre in genres:
        result[genre['id']] = genre['name']

    return result


MOVIE_GENERES = _get_movies_genres()


def return_movie_genres(genre_ids: list) -> str:
    result = ""
    for genre_id in genre_ids:
        result += f"{MOVIE_GENERES.get(genre_id, '')}, "
    return result


def get_movie_runtime(movie_id: int) -> int:
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    result = get_tmdb_response(url)
    return result.get('runtime', 0)


def get_popular_movies(list_len: int = 8) -> list:
    url = "https://api.themoviedb.org/3/movie/popular"
    result = get_tmdb_response(url)
    try:
        rand_movie_list = random.sample(result.get('results'), k=list_len)
        return rand_movie_list
    except ValueError:
        return result.get('results')[:list_len]


def get_poster_url(api_image_path: str, size: str = 'w342') -> str:
    secure_base_url = "https://image.tmdb.org/t/p/"
    return f"{secure_base_url}{size}{api_image_path}"
