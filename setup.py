import pandas as pd
import requests
from io import StringIO
from io import BytesIO
import gzip
import string
import re

def load_data (url):
    response = requests.get(url)
    with gzip.GzipFile(fileobj=BytesIO(response.content), mode='rb') as file:
        return pd.read_csv(file, sep='\t', na_values=["", "\\N", "NA"], low_memory=False)

def clean_title (title):
    title = title.lower()
    title = ' '.join(word.strip(string.punctuation) for word in title.split())
    return title

#load movie ratings
ratings_url = "https://datasets.imdbws.com/title.ratings.tsv.gz" 
ratings_df = load_data(ratings_url)

#load movie_titles
titles_url = "https://datasets.imdbws.com/title.basics.tsv.gz"
titles_df = load_data(titles_url)
titles_df = titles_df[titles_df['isAdult'] == 0] #select only kid friendly movies

#merge datasets on title id
merged_df = titles_df.merge(ratings_df, on='tconst') 

#select only holiday movies
merged_df['simpleTitle'] = merged_df['primaryTitle'].apply(clean_title)

holiday_movies = merged_df[(merged_df['titleType'].isin(['movie', 'video', 'tvMovie'])) & (
    merged_df['simpleTitle'].str.contains('holiday') |
    merged_df['simpleTitle'].str.contains('christmas') |
    merged_df['simpleTitle'].str.contains('xmas') |
    merged_df['simpleTitle'].str.contains('hanuk') |
    merged_df['simpleTitle'].str.contains('kwanzaa') |
    merged_df['simpleTitle'].str.contains(r"\bx mas\b") 
)].copy()
holiday_movies = holiday_movies.drop(columns=['endYear'])

#create boolean columns to specify which kind of holiday movie it is
holiday_movies['christmas'] = holiday_movies['simpleTitle'].str.contains('christmas').astype(int) |  holiday_movies['simpleTitle'].str.contains(r'x\s*mas').astype(int)
holiday_movies['hanukkah'] = holiday_movies['simpleTitle'].str.contains('hanuk').astype(int)
holiday_movies['kwanzaa'] = holiday_movies['simpleTitle'].str.contains('kwanzaa').astype(int)
holiday_movies['holiday'] = holiday_movies['simpleTitle'].str.contains('holiday').astype(int)
holiday_movies['isAdult'] = holiday_movies['isAdult'].astype(bool).astype(int)

#save titles and genres
holiday_movie_genres = holiday_movies[['tconst', 'genres']].copy()
holiday_movie_genres['genres'] = holiday_movie_genres['genres'].str.split(',')

holiday_movies.to_csv('holiday_movies.csv', index=False)
holiday_movie_genres.to_csv('holiday_genres.csv', index=False)
