"""Menu-driven Movie Rating Explorer for a beginner Python project."""

from analysis import filter_movies, sort_movies
from movie_manager import (
    add_movie,
    delete_movie,
    load_movies,
    save_movies,
    search_movies,
    update_movie,
)
from reports import display_movies, show_analysis_report, show_summary_report


def read_integer(prompt, minimum=None):
    """Keep asking until the user enters a whole number in the allowed range."""
    while True:
        try:
            value = int(input(prompt))
            if minimum is not None and value < minimum:
                print(f"Please enter a number that is at least {minimum}.")
                continue
            return value
        except ValueError:
            print("Please enter a whole number.")


def read_rating(prompt="Rating (0 to 10): "):
    """Read a decimal rating and check that it uses the project's 0-10 scale."""
    while True:
        try:
            rating = float(input(prompt))
            if 0 <= rating <= 10:
                return round(rating, 1)
            print("A rating must be between 0 and 10.")
        except ValueError:
            print("Please enter a number, such as 8.5.")


def collect_movie_details():
    """Collect one new movie and return its details in a dictionary."""
    movie_details = {
        "title": input("Movie title: ").strip(),
        "year": read_integer("Release year: ", minimum=1888),
        "genre": input("Genre: ").strip(),
        "director": input("Director: ").strip(),
        "runtime_min": read_integer("Runtime in minutes: ", minimum=1),
        "user_rating": read_rating(),
        "votes": read_integer("Number of ratings (enter 0 if unknown): ", minimum=0),
    }
    return movie_details


def show_menu():
    """Print the available project operations."""
    print("\n=== Movie Rating Explorer ===")
    print("1. Display all movies")
    print("2. Search by title, genre, or director")
    print("3. Add a movie")
    print("4. Update a movie")
    print("5. Delete a movie")
    print("6. Generate a summary report")
    print("7. Filter and sort movies")
    print("8. Show NumPy and Pandas analysis")
    print("0. Save and exit")


def update_one_movie(movies):
    """Ask which movie and field to update, then save the change."""
    movie_id = read_integer("Movie ID to update: ", minimum=1)
    print("Fields: 1 Title  2 Year  3 Genre  4 Director")
    print("        5 Runtime  6 Rating  7 Number of ratings")

    field_choices = {
        "1": "title",
        "2": "year",
        "3": "genre",
        "4": "director",
        "5": "runtime_min",
        "6": "user_rating",
        "7": "votes",
    }
    choice = input("Choose a field: ").strip()
    field_name = field_choices.get(choice)
    if field_name is None:
        print("That field choice is not available.")
        return movies

    if field_name == "year":
        new_value = read_integer("New release year: ", minimum=1888)
    elif field_name == "runtime_min":
        new_value = read_integer("New runtime in minutes: ", minimum=1)
    elif field_name == "votes":
        new_value = read_integer("New number of ratings: ", minimum=0)
    elif field_name == "user_rating":
        new_value = read_rating("New rating (0 to 10): ")
    else:
        new_value = input(f"New {field_name}: ").strip()
        if not new_value:
            print("The value cannot be blank.")
            return movies

    updated_movies, was_updated = update_movie(
        movies, movie_id, {field_name: new_value}
    )
    if was_updated:
        save_movies(updated_movies)
        print("Movie updated and saved.")
        return updated_movies

    print("No movie has that ID.")
    return movies


def main():
    """Run the interactive menu until the user chooses to exit."""
    movies = load_movies()
    print(f"Loaded {len(movies)} movie records.")

    while True:
        show_menu()
        choice = input("Select an option: ").strip()

        if choice == "1":
            display_movies(movies)
        elif choice == "2":
            keyword = input("Search text: ").strip()
            display_movies(search_movies(movies, keyword))
        elif choice == "3":
            movie_details = collect_movie_details()
            if not movie_details["title"]:
                print("A movie title is required. The record was not added.")
                continue
            movies = add_movie(movies, movie_details)
            save_movies(movies)
            print("Movie added and saved.")
        elif choice == "4":
            movies = update_one_movie(movies)
        elif choice == "5":
            movie_id = read_integer("Movie ID to delete: ", minimum=1)
            answer = input("Delete this record? (y/n): ").strip().lower()
            if answer == "y":
                movies, was_deleted = delete_movie(movies, movie_id)
                if was_deleted:
                    save_movies(movies)
                    print("Movie deleted and saved.")
                else:
                    print("No movie has that ID.")
        elif choice == "6":
            show_summary_report(movies)
        elif choice == "7":
            genre_text = input("Genre filter (press Enter for any genre): ").strip()
            minimum_text = input("Minimum rating (press Enter for none): ").strip()
            minimum_rating = None
            if minimum_text:
                try:
                    minimum_rating = float(minimum_text)
                except ValueError:
                    print("That rating was not a number; the rating filter is skipped.")

            filtered = filter_movies(
                movies,
                genre=genre_text or None,
                minimum_rating=minimum_rating,
            )
            sort_choice = input("Sort by rating or year? [rating/year]: ").strip().lower()
            sort_column = "year" if sort_choice == "year" else "user_rating"
            display_movies(sort_movies(filtered, sort_column))
        elif choice == "8":
            show_analysis_report(movies)
        elif choice == "0":
            save_movies(movies)
            print("Data saved. Goodbye!")
            break
        else:
            print("Please choose one of the menu options.")


if __name__ == "__main__":
    main()
