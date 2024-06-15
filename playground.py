import pandas as pd


def get_movies_and_att_dict(movies: pd.DataFrame):
    genres: list = movies["genres"].unique().tolist()
    genres_unique = set([item for sublist in genres for item in sublist.split(",")])

    titles: list = movies["title"]
    titles_lower: list = [title.lower() for title in titles]
    movies["title"] = titles_lower
    movies["genres"] = movies["genres"].tolist()

    return movies, {
        "genres": genres_unique,
        "language": movies["original_language"].unique(),
        "titles": list(set(titles_lower)),
    }


numeric_filtering_dict: dict = {
    "length": {
        "Any length": 0,
        "Short (up to 60 minutes)": 60,
        "Medium (60 to 90 minutes)": 75,
        "Long (more than 90 minutes)": 90
    },
    "rating": {
        "Any rating": 0,
        "Bad (below 4.5)": 4.5,
        "Decent (4.5 to 7.5)": 6.5,
        "Good (above 7.5)": 7.5,

    },
    "release_date": {
        'Any date': 0,
        "Old (before 1980)": 1980,
        "Recent (1981 to 2000)": 1995,
        "New (after 2000)": 2000
    }
}


def _filter_lang(movies, lang):
    filtered_df = movies[movies['original_language'] == lang]
    return filtered_df


def _filter_genres(movies, genre):
    movies['genres'] = movies['genres'].str.split(',')
    filtered_df = movies[movies['genres'].apply(lambda x: genre in x)]
    return filtered_df


def filter_numeric(movies, filter_by: str, textual_value, values_dict: dict):
    if values_dict[textual_value] == 0:
        return movies

    list_of_values: list = list(values_dict.values())
    list_of_values.remove(0)
    min_value = min(list_of_values)
    max_value = max(list_of_values)

    if values_dict[textual_value] == min_value:
        return movies[movies[filter_by] <= min_value]
    if values_dict[textual_value] == max_value:
        return movies[movies[filter_by] > max_value]

    return movies[(movies[filter_by] > min_value) & (movies[filter_by] <= max_value)]


def filter_movies(movies: pd.DataFrame, filters: dict):
    movies_filtered: pd.DataFrame = movies.copy()
    for filter_name, values_to_filter in filters.items():
        match filter_name:
            case "languages":
                if filters[filter_name]:
                    movies_filtered = _filter_lang(movies_filtered, filters[filter_name])
            case "genres":
                if filters[filter_name]:
                    movies_filtered = _filter_genres(movies_filtered, filters[filter_name])
            case "length":
                if filters[filter_name]:
                    movies_filtered = filter_numeric(movies_filtered, filter_name, filters[filter_name],
                                                     numeric_filtering_dict[filter_name])
            case "rating":
                if filters[filter_name]:
                    movies_filtered = filter_numeric(movies_filtered, filter_name, filters[filter_name],
                                                     numeric_filtering_dict[filter_name])
            case "release_date":
                if filters[filter_name]:
                    movies_filtered = filter_numeric(movies_filtered, filter_name, filters[filter_name],
                                                     numeric_filtering_dict[filter_name])
    return movies_filtered
