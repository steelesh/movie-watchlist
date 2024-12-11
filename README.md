# movie watchlist

## purpose

python script that allows users to manage a personal movie watchlist, in an easy and lightweight way using the command line. users can create, read, update, and delete movies from their list with arguments. [see usage](#usage)

## features
- validation: uses regex for title formatting, enumerated genres, and rating constraints
- persistence: uses sqlite, making it simple and portable, requiring no additional database configuration
- filtering: users can filter their list by ratings, genres, and watched status

## requirements
1. python 3.x

## build instructions
1. clone the repository and change into the directory
```bash
git clone https://github.com/steelesh/movie-watchlist.git && cd movie-watchlist
```
2. install the required packages:
```bash
pip install -r requirements.txt
```
3. run
```bash
python movie_watchlist.py [options]
```

## arguments

this script accepts the following arguments:
- -h: displays help and usage information
- --list: displays all movies in the watchlist
- --add: adds a new movie to the watchlist
- --delete <movie_title>: deletes a movie from the watchlist
- --update <movie_title>: updates the movie details
- --filter-rating <rating>: filters movies by rating
- --filter-genre <genre>: filters movies by genre
- --filter-watched <true|false>: filters movies by watched status

additional options when adding or updating movies:
- --title: specify the movie title (required for --add)
- --genre: specify the movie genre
- --rating: specify the movie rating (1-5)
- --watched: specify the watched status (true/false)

## usage

<details>
<summary>list all movies in the watchlist</summary>
<br />

**input**
```bash
python movie_watchlist.py --list
```

**output**
```bash
interstellar | scifi | 4 | No
inception | scifi | 4 | Yes
the dark knight | action | 5 | Yes
```
</details>

<details>
<summary>add a movie to the watchlist</summary>
<br />

**input**
```bash
python movie_watchlist.py --add --title "interstellar" --genre scifi --rating 4
```

**output**
```bash
"interstellar" added to watchlist
```
</details>

<details>
<summary>update a movie in the watchlist</summary>
<br />

**input**
```bash
python movie_watchlist.py --update "interstellar" --rating 5 --watched true
```

**output**
```bash
"interstellar" updated in watchlist
```
</details>

<details>
<summary>delete a movie from the watchlist</summary>
<br />

**input**
```bash
python movie_watchlist.py --delete "interstellar"
```

**output**
```bash
"interstellar" deleted from watchlist
```
</details>

<details>
<summary>filter movies by rating</summary>
<br />

**input**
```bash
python movie_watchlist.py --filter-rating 4
```

**output**
```bash
interstellar | scifi | 4 | No
inception | scifi | 4 | Yes
```
</details>

<details>
<summary>filter movies by genre</summary>
<br />

**input**
```bash
python movie_watchlist.py --filter-genre scifi
```

**output**
```bash
interstellar | scifi | 4 | No
inception| scifi | 5 | Yes
```
</details>

<details>
<summary>filter movies by watched status</summary>
<br />

**input**
```bash
python movie_watchlist.py --filter-watched true
```

**output**
```bash
interstellar | scifi | 4 | Yes
inception | scifi | 5 | Yes
the dark knight | action | 5 | Yes
```
</details>


## validation
- movie titles must be 1-100 characters. can contain letters, numbers, spaces, and basic punctuation
- genres must be one of the following: action, comedy, drama, horror, scifi, thriller
- ratings must be between 1 and 5
- watched status must be either true or false

## license
>you can check out the full license [here](https://github.com/steelesh/movie-watchlist/blob/main/LICENSE)

this project is licensed under the terms of the **MIT** license
