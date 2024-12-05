import argparse
import sqlite3
import re
import sys
from typing import Optional, Dict, Any

# constants
VALID_GENRES = ['action', 'comedy', 'drama', 'horror', 'scifi', 'thriller']

# initialize cursor & connect to db
conn = sqlite3.connect('watchlist.db')
cursor = conn.cursor()

# create movies table if it doesn't exist
def setup_database():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            title TEXT PRIMARY KEY,
            genre TEXT NOT NULL,
            rating INTEGER NOT NULL,
            watched BOOLEAN NOT NULL DEFAULT FALSE
        )
    ''')
    conn.commit()

# validates title using regex
def validate_title(title: str) -> bool:
    pattern = r'^[\w\s\-.,\'\":!?()]{1,100}$'
    return bool(re.match(pattern, title))

# validates rating is between 1 and 5
def validate_rating(rating: int) -> bool:
    return 1 <= rating <= 5

# validates genre is in specified list
def validate_genre(genre: str) -> bool:
    return genre.lower() in VALID_GENRES

# adds a new movie
def add_movie(title: str, genre: str, rating: int, watched: bool = False) -> bool:
    if not validate_title(title):
        print("err: invalid title format")
        return None
    if not validate_genre(genre):
        print(f"err: invalid genre. must be one of: {', '.join(VALID_GENRES)}")
        return None
    if not validate_rating(rating):
        print("err: rating must be between 1 and 5")
        return None

    try:
        cursor.execute(
            'INSERT INTO movies (title, genre, rating, watched) VALUES (?, ?, ?, ?)',
            (title, genre.lower(), rating, watched)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print(f"err: \"{title}\" already exists in watchlist")
    except sqlite3.Error as e:
        print(f"err: {e}")
    return None

# deletes an existing movie
def delete_movie(title: str) -> bool:
    try:
        cursor.execute('DELETE FROM movies WHERE title = ?', (title,))
        if cursor.rowcount == 0:
            print(f"err: \"{title}\" not found in watchlist")
            return None
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"err: {e}")
        return None

# updates an existing movie
def update_movie(title: str, updates: Dict[str, Any]) -> bool:
    if 'rating' in updates and not validate_rating(updates['rating']):
        print("err: rating must be between 1 and 5")
        return None
    if 'genre' in updates and not validate_genre(updates['genre']):
        print(f"err: invalid genre. must be one of: {', '.join(VALID_GENRES)}")
        return None

    try:
        current = cursor.execute('SELECT * FROM movies WHERE title = ?', (title,)).fetchone()
        if not current:
            print(f"err: \"{title}\" not found in watchlist")
            return None

        fields = []
        vals = []
        for key, value in updates.items():
            fields.append(f"{key} = ?")
            vals.append(value)
        vals.append(title)

        cursor.execute(f'UPDATE movies SET {", ".join(fields)} WHERE title = ?', vals)
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"err: {e}")
        return None

# lists movies with optional filters
def list_movies(rating: Optional[int] = None, genre: Optional[str] = None, watched: Optional[bool] = None) -> list:
    try:
        q = 'SELECT * FROM movies'
        params = []
        conditions = []

        if rating is not None:
            conditions.append('rating = ?')
            params.append(rating)
        if genre is not None:
            conditions.append('LOWER(genre) = LOWER(?)')
            params.append(genre)
        if watched is not None:
            conditions.append('watched = ?')
            params.append(watched)

        if conditions:
            q += ' WHERE ' + ' AND '.join(conditions)

        cursor.execute(q, params)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"err: {e}")
        return None

# parses command line args
def parse_args():
    parser = argparse.ArgumentParser()
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list', action='store_true', help='list all movies')
    group.add_argument('--add', action='store_true', help='add a new movie')
    group.add_argument('--update', help='update a movie')
    group.add_argument('--delete', help='delete a movie')
    
    parser.add_argument('--filter-rating', type=int, help='filter by rating (1-5)')
    parser.add_argument('--filter-genre', help='filter by genre')
    parser.add_argument('--filter-watched', type=lambda x: x.lower() == 'true', help='filter by watched status (true/false)')
    
    parser.add_argument('--title', help='movie title (required for --add)')
    parser.add_argument('--genre', help='movie genre')
    parser.add_argument('--rating', type=int, help='movie rating (1-5)')
    parser.add_argument('--watched', type=lambda x: x.lower() == 'true', help='watched status (true/false)')

    return parser.parse_args()

# main function
def main():
    args = parse_args()
    setup_database()

    try:
        if args.list or any(filter_arg is not None for filter_arg in [args.filter_rating, args.filter_genre, args.filter_watched]):
            movies = list_movies(
                rating=args.filter_rating,
                genre=args.filter_genre,
                watched=args.filter_watched
            )
            if movies is None:
                return
            if not movies:
                print("no movies found")
                return
            for movie in movies:
                print(f"{movie[0]} | {movie[1]} | {movie[2]} | {'Yes' if movie[3] else 'No'}")

        elif args.add:
            if not args.title:
                print("err: --title is required when adding a movie")
                return
            if not args.genre:
                print("err: --genre is required when adding a movie")
                return
            if not args.rating:
                print("err: --rating is required when adding a movie")
                return
            
            result = add_movie(
                args.title,
                args.genre,
                args.rating,
                args.watched if args.watched is not None else False
            )
            if result:
                print(f"\"{args.title}\" added to watchlist")

        elif args.delete:
            result = delete_movie(args.delete)
            if result:
                print(f"\"{args.delete}\" deleted from watchlist")

        elif args.update:
            updates = {}
            if args.genre is not None:
                updates['genre'] = args.genre
            if args.rating is not None:
                updates['rating'] = args.rating
            if args.watched is not None:
                updates['watched'] = args.watched

            if not updates:
                print("err: no updates provided")
                return
            
            result = update_movie(args.update, updates)
            if result:
                print(f"\"{args.update}\" updated in watchlist")

    except Exception as e:
        print(f"err: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    main()
