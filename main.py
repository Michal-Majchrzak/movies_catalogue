from flask import Flask, render_template, request
from movies_catalogue import tmdb_client


app = Flask(__name__)
LIST_TYPES = ['now_playing', 'popular', 'top_rated', 'upcoming']
#tmdb_client.MOVIE_GENERES = tmdb_client.build_movies_genres_dict_from_tmdb_api()


@app.route('/', methods=['GET'])
def homepage():
    passed_list = request.args.get('list_type', '')

    if passed_list in LIST_TYPES:
        selected_list = passed_list
    else:
        selected_list = 'popular'

    movies = tmdb_client.get_movies_list(selected_list, 8)
    return render_template('homepage.html', movies=movies, list_types=LIST_TYPES, selected=selected_list)


@app.route('/movie/<int:movie_id>', methods=['GET'])
def movie_details(movie_id: int):
    movie = tmdb_client.get_single_movie(movie_id)
    cast = tmdb_client.get_single_movie_cast(movie_id, 8)

    backdrop = tmdb_client.get_random_movie_backdrop(movie_id)
    if backdrop:
        movie['backdrop_path'] = backdrop

    return render_template("movie_details.html", movie=movie, cast=cast)


@app.context_processor
def utility_processor():
    def tmdb_image_url(path: str, size: str):
        return tmdb_client.get_poster_url(path, size)
    return {"tmdb_image_url": tmdb_image_url}


@app.context_processor
def utility_processor():
    def tmdb_movie_runtime(movie_id: int):
        return tmdb_client.get_movie_runtime(movie_id)
    return {"tmdb_movie_runtime": tmdb_movie_runtime}


@app.context_processor
def utility_processor():
    def tmdb_return_genres(genre_ids: list):
        return tmdb_client.return_movie_genres(genre_ids)
    return {"tmdb_return_genres": tmdb_return_genres}

