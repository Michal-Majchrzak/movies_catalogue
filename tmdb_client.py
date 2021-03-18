import requests
import random

V4_TOKEN = ""
MOVIE_GENERES = []


def get_tmdb_response(url: str) -> dict:
    headers = {'Authorization': f"Bearer {V4_TOKEN}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def build_movies_genres_dict_from_tmdb_api() -> dict:
    url = "https://api.themoviedb.org/3/genre/movie/list"
    genres = get_tmdb_response(url).get('genres')
    result = {}

    try:
        for genre in genres:
            result[genre['id']] = genre['name']
    except TypeError:
        return {}

    return result


def return_movie_genres(genre_ids: list) -> str:
    genre_list = []
    for genre_id in genre_ids:
        genre_name = MOVIE_GENERES.get(genre_id)
        if genre_name:
            genre_list.append(genre_name)

    result = ', '.join(genre_list)
    return result


def get_movie_runtime(movie_id: int) -> int:
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    result = get_tmdb_response(url)
    return result.get('runtime', 0)


def get_random_movie_backdrop(movie_id: int) -> str:
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/images"
    result = get_tmdb_response(url).get('backdrops', [])
    index = random.randint(0, len(result))
    try:
        if index == len(result):
            index -= 1
        return result[index].get('file_path', '')
    except IndexError:
        return []


def get_single_movie(movie_id: int) -> dict:
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    result = get_tmdb_response(url)
    return result


def get_single_movie_cast(movie_id: int, list_len: int = 4) -> list:
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    result = get_tmdb_response(url)
    return result.get('cast', [])[:list_len]


def get_movies_list(list_name: str = 'popular', list_len: int = 8) -> list:
    url = f"https://api.themoviedb.org/3/movie/{list_name}"
    result = get_tmdb_response(url)
    try:
        rand_movie_list = random.sample(result.get('results'), k=list_len)
        return rand_movie_list
    except ValueError:
        return result.get('results')[:list_len]


def get_poster_url(api_image_path: str, size: str = 'w342') -> str:
    secure_base_url = "https://image.tmdb.org/t/p/"
    return f"{secure_base_url}{size}{api_image_path}"
