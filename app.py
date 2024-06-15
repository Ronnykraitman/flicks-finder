from flask import Flask, render_template, request, jsonify
import os
import pandas as pd
from model import get_recommend_movies_based_on_plot
from playground import numeric_filtering_dict, get_movies_and_att_dict

app = Flask(__name__)


script_dir = os.path.dirname(__file__)
relative_path = os.path.join(script_dir, "data/imdb_movies.csv")
data: pd.DataFrame = pd.read_csv(relative_path)
movies, movies_att = get_movies_and_att_dict(data)


@app.route("/")
def home():
    return render_template("welcome.html")


@app.route('/explore', methods=['GET', 'POST'])
def redirect_to_explore():
    options_genres = movies_att["genres"]
    options_language = movies_att["language"]
    options_title = movies_att["titles"]

    return render_template('explore.html',options_title=options_title, options_genres=options_genres, options_language=options_language,
                           options_movie_length=list(numeric_filtering_dict["length"].keys()), options_movie_rating=list(numeric_filtering_dict["rating"].keys()), options_movie_date=list(numeric_filtering_dict["release_date"].keys()))


@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    options_title = movies_att["titles"]
    query = request.args.get('query', '').lower()
    matching_options = [option for option in options_title if query in option.lower()]
    return jsonify(matching_options)


@app.route('/recommendation', methods=['POST'])
def submit_form():
    selected_title = request.form.get('moviesInput')
    selected_genres = request.form.get('genre_selection')
    selected_languages = request.form.get('lng_selection')
    selected_length = request.form.get('movie_length_selection')
    selected_rating = request.form.get('rating_selection')
    selected_date = request.form.get('date_selection')

    filters: dict = {
        "title": selected_title,
        "languages": selected_languages,
        "genres": selected_genres,
        "length": selected_length,
        "rating": selected_rating,
        "release_date": selected_date

    }

    recommended_movies: list = get_recommend_movies_based_on_plot(movies, filters)
    if recommended_movies:
        winner = recommended_movies[0]
        other_movies = recommended_movies[1:]
        return render_template("results.html", winner=winner.title(), other_movies=other_movies)
    else:
        return render_template("no_results.html")



if __name__ == "__main__":
    app.run(port=8000)
