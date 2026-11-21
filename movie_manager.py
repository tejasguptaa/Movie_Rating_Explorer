"""CSV loading and Create, Read, Update, Delete operations for movie records."""

from pathlib import Path

import pandas as pd


COLUMNS = (
    "movie_id",
    "title",
    "year",
    "genre",
    "director",
    "runtime_min",
    "user_rating",
    "votes",
)
DATA_FILE = Path(__file__).resolve().parent / "data" / "movies.csv"


def load_movies(file_path=DATA_FILE):
    """Read the CSV file and fill missing values with simple safe defaults."""
    try:
        movies = pd.read_csv(file_path)
    except FileNotFoundError:
        movies = pd.DataFrame(columns=COLUMNS)

    for column in COLUMNS:
        if column not in movies.columns:
            movies[column] = pd.NA

    movies = movies.loc[:, list(COLUMNS)].copy()
    movies["title"] = movies["title"].fillna("Untitled").astype(str)
    movies["genre"] = movies["genre"].fillna("Unknown").astype(str)
    movies["director"] = movies["director"].fillna("Unknown").astype(str)

    for column in ("movie_id", "year", "runtime_min", "user_rating", "votes"):
        movies[column] = pd.to_numeric(movies[column], errors="coerce")

    if movies["movie_id"].isna().any():
        movies["movie_id"] = movies["movie_id"].fillna(0)
    if movies["year"].isna().any():
        movies["year"] = movies["year"].fillna(0)
    if movies["runtime_min"].isna().any():
        runtime_median = movies["runtime_min"].median()
        movies["runtime_min"] = movies["runtime_min"].fillna(
            0 if pd.isna(runtime_median) else runtime_median
        )
    if movies["user_rating"].isna().any():
        rating_median = movies["user_rating"].median()
        movies["user_rating"] = movies["user_rating"].fillna(
            0 if pd.isna(rating_median) else rating_median
        )
    movies["votes"] = movies["votes"].fillna(0)

    for column in ("movie_id", "year", "runtime_min", "votes"):
        movies[column] = movies[column].astype(int)
    movies["user_rating"] = movies["user_rating"].astype(float)
    return movies.sort_values("movie_id").reset_index(drop=True)


def save_movies(movies, file_path=DATA_FILE):
    """Write the current DataFrame back to its CSV file."""
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    movies.loc[:, list(COLUMNS)].to_csv(file_path, index=False)


def add_movie(movies, movie_details):
    """Add a movie using a dictionary of its field values."""
    movie_record = {
        "movie_id": int(movies["movie_id"].max()) + 1 if not movies.empty else 1,
        "title": movie_details.get("title", "Untitled"),
        "year": movie_details.get("year", 0),
        "genre": movie_details.get("genre", "Unknown") or "Unknown",
        "director": movie_details.get("director", "Unknown") or "Unknown",
        "runtime_min": movie_details.get("runtime_min", 0),
        "user_rating": movie_details.get("user_rating", 0),
        "votes": movie_details.get("votes", 0),
    }
    return pd.concat([movies, pd.DataFrame([movie_record])], ignore_index=True)


def search_movies(movies, keyword):
    """Find matching titles, genres, or directors without case sensitivity."""
    search_columns = []
    search_columns.append("title")
    search_columns.append("genre")
    search_columns.append("director")
    keyword = str(keyword).strip()
    if not keyword:
        return movies.copy()

    matches = pd.Series(False, index=movies.index)
    for column in search_columns:
        matches = matches | movies[column].astype(str).str.contains(
            keyword, case=False, na=False, regex=False
        )
    return movies.loc[matches].reset_index(drop=True)


def update_movie(movies, movie_id, updates):
    """Apply one or more field changes to the record with the selected ID."""
    editable_fields = set(COLUMNS) - {"movie_id"}
    if not updates or any(field not in editable_fields for field in updates):
        return movies.copy(), False

    matching_rows = movies.index[movies["movie_id"] == movie_id]
    if len(matching_rows) == 0:
        return movies.copy(), False

    updated_movies = movies.copy()
    row_index = matching_rows[0]
    for field, value in updates.items():
        updated_movies.loc[row_index, field] = value
    return updated_movies, True


def delete_movie(movies, movie_id):
    """Remove a record by ID and return the new table plus a success flag."""
    remaining = movies.loc[movies["movie_id"] != movie_id].copy()
    was_deleted = len(remaining) != len(movies)
    return remaining.reset_index(drop=True), was_deleted
