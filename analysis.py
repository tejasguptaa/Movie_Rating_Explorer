"""Pandas filters and NumPy/Pandas analysis for the Movie Rating Explorer."""

import numpy as np
import pandas as pd


def filter_movies(movies, genre=None, minimum_rating=None):
    """Return records matching an optional genre and minimum rating."""
    filtered = movies.copy()
    if genre:
        filtered = filtered.loc[
            filtered["genre"].astype(str).str.contains(
                genre, case=False, na=False, regex=False
            )
        ]
    if minimum_rating is not None:
        filtered = filtered.loc[filtered["user_rating"] >= minimum_rating]
    return filtered.reset_index(drop=True)


def sort_movies(movies, column="user_rating", descending=True):
    """Sort a DataFrame by rating, year, or another valid column."""
    if column not in movies.columns:
        raise ValueError(f"Cannot sort by unknown column: {column}")
    return movies.sort_values(
        by=column, ascending=not descending
    ).reset_index(drop=True)


def numpy_rating_analysis(movies):
    """Build 1D/2D NumPy arrays and calculate common rating statistics."""
    rating_array = np.array(movies["user_rating"].to_numpy(dtype=float))
    year_rating_array = movies[["year", "user_rating"]].to_numpy(dtype=float)

    if rating_array.size == 0:
        return {
            "rating_array": rating_array,
            "year_rating_array": year_rating_array,
            "first_rating": None,
            "first_five_ratings": rating_array[:5],
            "first_year_rating": None,
            "first_five_rows": year_rating_array[:5, :],
            "sum": 0.0,
            "mean": None,
            "maximum": None,
            "minimum": None,
            "standard_deviation": None,
        }

    first_rating = rating_array[0]
    first_five_ratings = rating_array[:5]
    first_year_rating = year_rating_array[0, 1]
    first_five_rows = year_rating_array[:5, :]

    return {
        "rating_array": rating_array,
        "year_rating_array": year_rating_array,
        "first_rating": first_rating,
        "first_five_ratings": first_five_ratings,
        "first_year_rating": first_year_rating,
        "first_five_rows": first_five_rows,
        "sum": float(np.sum(rating_array)),
        "mean": float(np.mean(rating_array)),
        "maximum": float(np.max(rating_array)),
        "minimum": float(np.min(rating_array)),
        "standard_deviation": float(np.std(rating_array)),
    }


def genre_group_summary(movies):
    """Group rows by genre and calculate count, average rating, and runtime."""
    if movies.empty:
        return pd.DataFrame(
            columns=["genre", "movie_count", "average_rating", "average_runtime"]
        )

    grouped = movies.groupby("genre", dropna=False).agg(
        movie_count=("movie_id", "count"),
        average_rating=("user_rating", "mean"),
        average_runtime=("runtime_min", "mean"),
    )
    return grouped.reset_index().sort_values("average_rating", ascending=False)


def pandas_rating_statistics(movies):
    """Return Pandas descriptive statistics for the user rating column."""
    if movies.empty:
        return pd.Series(dtype=float)
    return movies["user_rating"].describe()
