from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', methods=['GET'])
def homepage():
    movies = range(8)
    return render_template('homepage.html', movies=movies)


if __name__ == '__main__':
    app.run(debug=True)