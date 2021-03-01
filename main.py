from flask import Flask, render_template
import tmdb_client

app = Flask(__name__)


@app.route('/', methods=['GET'])
def homepage():
    movies = tmdb_client.get_popular_movies(8)
    return render_template('homepage.html', movies=movies)


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


if __name__ == '__main__':
    app.run(debug=True)