"""Readable terminal tables and analysis reports."""

from analysis import genre_group_summary, numpy_rating_analysis, pandas_rating_statistics


def display_movies(movies):
    """Display selected movie columns in a compact terminal table."""
    if movies.empty:
        print("No movie records matched.")
        return

    # A list selects the columns we want readers to see in this table.
    display_columns = ["movie_id", "title", "year", "genre", "user_rating"]
    print(movies.loc[:, display_columns].to_string(index=False))
    print(f"\nRecords shown: {len(movies)}")


def show_summary_report(movies):
    """Print a short overview, plus a genre comparison table."""
    print("\n=== Movie Collection Summary ===")
    if movies.empty:
        print("There are no records to summarize yet.")
        return

    # A set keeps one copy of each genre so we can count unique categories.
    unique_genres = set(movies["genre"].dropna().astype(str))
    average_rating = movies["user_rating"].mean()
    print(f"Total movie records: {len(movies)}")
    print(f"Unique genres: {len(unique_genres)} ({', '.join(sorted(unique_genres))})")
    print(f"Average rating: {average_rating:.2f} / 10")
    print(f"Release years: {movies['year'].min()} to {movies['year'].max()}")

    top_movies = movies.sort_values("user_rating", ascending=False).head(5)
    print("\nTop 5 ratings in this sample:")
    display_movies(top_movies)

    print("\nAverage rating and runtime by genre:")
    grouped = genre_group_summary(movies).copy()
    if not grouped.empty:
        grouped["average_rating"] = grouped["average_rating"].round(2)
        grouped["average_runtime"] = grouped["average_runtime"].round(1)
        print(grouped.to_string(index=False))


def show_analysis_report(movies):
    """Demonstrate NumPy arrays and Pandas analysis with readable examples."""
    print("\n=== NumPy and Pandas Analysis ===")
    if movies.empty:
        print("Add a movie first so there is data to analyze.")
        return

    numpy_results = numpy_rating_analysis(movies)
    print("NumPy 1D rating array (first five values):")
    print(numpy_results["first_five_ratings"])
    print(f"First rating by index: {numpy_results['first_rating']:.1f}")
    print(f"Sum: {numpy_results['sum']:.2f}")
    print(f"Mean: {numpy_results['mean']:.2f}")
    print(f"Maximum: {numpy_results['maximum']:.1f}")
    print(f"Minimum: {numpy_results['minimum']:.1f}")
    print(f"Standard deviation: {numpy_results['standard_deviation']:.2f}")
    print("\nNumPy 2D array (year, rating), first five rows from a slice:")
    print(numpy_results["first_five_rows"])
    print(f"Rating selected from the 2D array by [row 0, column 1]: {numpy_results['first_year_rating']:.1f}")

    print("\nPandas selected rows and columns (first five movies):")
    selected_columns = ["title", "year", "genre", "user_rating"]
    print(movies.loc[:, selected_columns].head(5).to_string(index=False))
    print("\nPandas rating statistics (describe):")
    print(pandas_rating_statistics(movies).round(2).to_string())

    print("\nPandas GroupBy average rating by genre:")
    grouped = genre_group_summary(movies)
    if not grouped.empty:
        print(grouped[["genre", "movie_count", "average_rating"]].round(2).to_string(index=False))
