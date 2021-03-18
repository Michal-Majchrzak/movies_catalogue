from movies_catalogue import tmdb_client
from unittest.mock import Mock
import pytest


def test_get_movie_runtime_result_value(monkeypatch):
    result = 95
    tmdb_response = {'runtime': 95}

    get_tmdb_response_mock = Mock()
    get_tmdb_response_mock.return_value = tmdb_response
    monkeypatch.setattr('movies_catalogue.tmdb_client.get_tmdb_response', get_tmdb_response_mock)
    assert tmdb_client.get_movie_runtime(0) == result


def test_get_movie_runtime_endpoint(monkeypatch):
    result = "https://api.themoviedb.org/3/movie/123456"

    get_tmdb_response_mock = Mock()
    monkeypatch.setattr('movies_catalogue.tmdb_client.get_tmdb_response', get_tmdb_response_mock)

    tmdb_client.get_movie_runtime(123456)
    assert result in get_tmdb_response_mock.call_args.args


def test_get_random_movie_backdrop(monkeypatch):
    result = 'some-backdrop-file-path'
    tmdb_response = {'backdrops': [{'file_path': 'some-backdrop-file-path'}]}

    get_tmdb_response_mock = Mock()
    get_tmdb_response_mock.return_value = tmdb_response
    monkeypatch.setattr('movies_catalogue.tmdb_client.get_tmdb_response', get_tmdb_response_mock)

    assert tmdb_client.get_random_movie_backdrop(0) == result


def test_get_random_movie_backdrop_empty_list(monkeypatch):
    result = ''

    get_tmdb_response_mock = Mock()
    get_tmdb_response_mock.return_value = {}
    monkeypatch.setattr('movies_catalogue.tmdb_client.get_tmdb_response', get_tmdb_response_mock)

    assert tmdb_client.get_random_movie_backdrop(123) == result


def test_get_random_movie_backdrop_endpoint(monkeypatch):
    result = "https://api.themoviedb.org/3/movie/123/images"

    get_tmdb_response_mock = Mock()
    get_tmdb_response_mock.return_value = {}
    monkeypatch.setattr('movies_catalogue.tmdb_client.get_tmdb_response', get_tmdb_response_mock)

    tmdb_client.get_random_movie_backdrop(123)
    assert result in get_tmdb_response_mock.call_args.args


def test_get_single_movie(monkeypatch):
    result = {'title': 'movie'}

    get_tmdb_response_mock = Mock()
    get_tmdb_response_mock.return_value = result
    monkeypatch.setattr('movies_catalogue.tmdb_client.get_tmdb_response', get_tmdb_response_mock)

    assert tmdb_client.get_single_movie(0) == result


def test_get_single_endpoint(monkeypatch):
    result = "https://api.themoviedb.org/3/movie/234"

    get_tmdb_response_mock = Mock()
    monkeypatch.setattr('movies_catalogue.tmdb_client.get_tmdb_response', get_tmdb_response_mock)

    tmdb_client.get_single_movie(234)
    assert result in get_tmdb_response_mock.call_args.args


def test_get_single_movie_cast_without_list_len(monkeypatch):
    result = ['CastMember1', 'CastMember2', 'CastMember3', 'CastMember4', 'CastMember5']
    tmdb_response = {'cast': result}

    get_tmdb_response_mock = Mock()
    get_tmdb_response_mock.return_value = tmdb_response
    monkeypatch.setattr('movies_catalogue.tmdb_client.get_tmdb_response', get_tmdb_response_mock)

    assert tmdb_client.get_single_movie_cast(0) == result[:4]


@pytest.mark.parametrize("list_len", [1, 2, 3, 4, 5])
def test_get_single_movie_cast_with_list_len(monkeypatch, list_len):
    result = ['CastMember1', 'CastMember2', 'CastMember3', 'CastMember4', 'CastMember5']
    tmdb_response = {'cast': result}

    get_tmdb_response_mock = Mock()
    get_tmdb_response_mock.return_value = tmdb_response
    monkeypatch.setattr('movies_catalogue.tmdb_client.get_tmdb_response', get_tmdb_response_mock)

    assert tmdb_client.get_single_movie_cast(0, list_len) == result[:list_len]


def test_get_single_movie_cast_endpoint(monkeypatch):
    result = "https://api.themoviedb.org/3/movie/12/credits"

    get_tmdb_response_mock = Mock()
    get_tmdb_response_mock.return_value = {'cast': []}
    monkeypatch.setattr('movies_catalogue.tmdb_client.get_tmdb_response', get_tmdb_response_mock)

    tmdb_client.get_single_movie_cast(12)
    assert result in get_tmdb_response_mock.call_args.args


def test_get_movies_list_without_params(monkeypatch):
    result = ['Movie1', 'Movie2', 'Movie3', 'Movie4', 'Movie5', 'Movie6']
    tmdb_response = {'results': result}

    get_tmdb_response_mock = Mock()
    get_tmdb_response_mock.return_value = tmdb_response
    monkeypatch.setattr('movies_catalogue.tmdb_client.get_tmdb_response', get_tmdb_response_mock)

    assert tmdb_client.get_movies_list() == result


@pytest.mark.parametrize("list_length", [1, 2, 3, 4])
def test_get_movies_list_list_length(monkeypatch, list_length):
    result = ['Movie1', 'Movie2', 'Movie3', 'Movie4', 'Movie5', 'Movie6']
    tmdb_response = {'results': result}

    get_tmdb_response_mock = Mock()
    get_tmdb_response_mock.return_value = tmdb_response
    monkeypatch.setattr('movies_catalogue.tmdb_client.get_tmdb_response', get_tmdb_response_mock)

    assert len(tmdb_client.get_movies_list(list_len=list_length)) == list_length


@pytest.mark.parametrize("list_name", ['popular', 'top_rated', 'now_playing'])
def test_get_movies_list_with_list_name(monkeypatch, list_name):
    result = f"https://api.themoviedb.org/3/movie/{list_name}"

    get_tmdb_response_mock = Mock()
    get_tmdb_response_mock.return_value = {'results': []}
    monkeypatch.setattr('movies_catalogue.tmdb_client.get_tmdb_response', get_tmdb_response_mock)

    tmdb_client.get_movies_list(list_name=list_name)
    assert result in get_tmdb_response_mock.call_args.args


def test_get_poster_url_uses_default_size():
    poster_api_path = 'some-poster-path'
    expected_default_size = 'w342'

    poster_url = tmdb_client.get_poster_url(api_image_path=poster_api_path)
    assert expected_default_size in poster_url


@pytest.mark.parametrize("size", ['w320', 'w500', 'w234'])
def test_get_poster_url_uses_size_from_param(size: str):
    poster_api_path = 'some-poster-path'

    poster_url = tmdb_client.get_poster_url(api_image_path=poster_api_path, size=size)
    assert size in poster_url


@pytest.mark.parametrize("genre_ids, expected_result",
                         [
                             ([1, 2], 'genre1, genre2'),
                             ([2, 3], 'genre2, genre3'),
                             ([1, 3], 'genre1, genre3'),
                             ([1, 5], 'genre1'),
                             ([], "")
                         ]
                         )
def test_return_movie_genres(monkeypatch, genre_ids, expected_result):
    genres = {1: 'genre1', 2: 'genre2', 3: 'genre3'}
    monkeypatch.setattr('movies_catalogue.tmdb_client.MOVIE_GENERES', genres)

    assert tmdb_client.return_movie_genres(genre_ids) == expected_result


@pytest.mark.parametrize("tmdb_response, expected_output",
                         [
                             (
                                     {"genres": [{'id': 1, 'name': 'genre1'}]},
                                     {1: 'genre1'}
                             ),
                             (
                                    {},
                                    {}
                             )
                         ]
                         )
def test_build_movies_genres_dict_from_tmdb_api(monkeypatch, tmdb_response, expected_output):
    get_tmdb_response_mock = Mock()
    get_tmdb_response_mock.return_value = tmdb_response
    monkeypatch.setattr('movies_catalogue.tmdb_client.get_tmdb_response', get_tmdb_response_mock)

    assert tmdb_client.build_movies_genres_dict_from_tmdb_api() == expected_output


def test_get_tmdb_response(monkeypatch):
    movie_list = ['Movie1', 'Movie2']

    requests_get_mock = Mock()
    response = requests_get_mock.return_value
    response.json.return_value = movie_list
    monkeypatch.setattr('movies_catalogue.tmdb_client.requests.get', requests_get_mock)

    assert tmdb_client.get_tmdb_response('') == movie_list


@pytest.mark.parametrize("token",
                         [
                             "some-token",
                             "some-other_token"
                         ]
                         )
def test_get_tmdb_response_header_param(monkeypatch, token):
    expected_result = {'Authorization': f"Bearer {token}"}
    tmdb_client_global_token = token

    requests_get_mock = Mock()
    response = requests_get_mock.return_value
    response.json.return_value = []

    monkeypatch.setattr('movies_catalogue.tmdb_client.V4_TOKEN', tmdb_client_global_token)
    monkeypatch.setattr('movies_catalogue.tmdb_client.requests.get', requests_get_mock)

    tmdb_client.get_tmdb_response('')

    assert expected_result == requests_get_mock.call_args.kwargs.get('headers')