# Movie Rating Explorer

Movie Rating Explorer is a beginner-friendly, terminal-based Python project for exploring a small movie collection. You can add, display, search, update, and delete records, then use NumPy and Pandas to summarize the ratings. The code includes comments that explain the main learning ideas.

## What the project demonstrates

- A CSV dataset with **60 starter movie records** before changes made through the app.
- Create, Read, Update, and Delete operations.
- Searching by movie title, genre, or director.
- Filtering by genre or minimum rating, and sorting by rating or year.
- A summary report with unique genres, top ratings, and genre averages.
- NumPy 1D and 2D arrays, indexing, slicing, sum, mean, maximum, minimum, and standard deviation.
- Pandas DataFrame creation from a CSV, selected rows and columns, filtering, sorting, `groupby`, missing-value handling, and descriptive statistics.
- Four Python modules: `main.py`, `movie_manager.py`, `analysis.py`, and `reports.py`.

The included titles are practice examples. Their ratings and vote counts are illustrative training data, not verified audience ratings or recommendations. The CSV includes a few blank example values so the missing-value handling can be observed when the program loads it.

## Run the project

You need Python 3, NumPy, and Pandas. From this folder, create an environment and install the listed packages:

```bash
python -m venv .venv
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

Install the packages and start the menu:

```bash
pip install -r requirements.txt
python main.py
```

The menu and reports appear in the VS Code terminal. Changes are saved to `data/movies.csv`.

## Project files

| File | Purpose |
| --- | --- |
| `main.py` | Prints the menu, accepts input, and connects the modules. |
| `movie_manager.py` | Loads and saves the CSV, handles missing values, and performs movie record operations. |
| `analysis.py` | Filters and sorts records and performs NumPy and Pandas analysis. |
| `reports.py` | Displays movie tables and summary reports in the terminal. |
| `data/movies.csv` | The 60-row practice dataset. |
| `requirements.txt` | Lists the required third-party packages. |

## Python concepts used

The project uses more than five data-structure concepts from the training topics:

| Concept | Example in the project |
| --- | --- |
| Tuple | `COLUMNS` keeps the fixed set of CSV column names. |
| List | Search and display columns are stored in lists. |
| List method | `search_columns.append(...)` adds searchable fields. |
| Set | `editable_fields` and the unique genre list use sets. |
| Dictionary | Movie records and menu choices use key/value pairs. |
| Dictionary methods | `.get()` reads optional values and `.items()` applies updates. |

## Missing values

When the CSV is loaded, missing titles become `Untitled`; missing genres and directors become `Unknown`; missing ratings and runtimes use the column median; missing vote counts use `0`. Missing IDs or years use `0` so the row can still be read and reviewed. New records entered through the menu are checked for required values and numeric ranges.

## Requirements checklist

| Training requirement | Where to find it |
| --- | --- |
| At least 50 records | `data/movies.csv` starts with 60 practice records; added records are saved there. |
| Five data-structure concepts | `movie_manager.py`, `main.py`, `reports.py`, and the concept table above. |
| At least five user-defined functions | Functions are defined across all four Python modules. |
| NumPy 1D/2D arrays, indexing, slicing, and statistics | `analysis.py` and the menu's NumPy/Pandas analysis report. |
| Pandas DataFrame, CSV input, selected rows/columns, filters, sorting, GroupBy, missing values, statistics | `movie_manager.py`, `analysis.py`, and `reports.py`. |
| Three separate imported modules | `main.py` imports `movie_manager`, `analysis`, and `reports`. |
| File handling | `movie_manager.py` reads and writes `data/movies.csv`. |
| Add, display, search, update, delete, summary report | Menu options 1 through 6. |
| Clear terminal output | `reports.py` prints labeled tables and summaries. |
