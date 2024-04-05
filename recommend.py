import model as mod
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics.pairwise import cosine_similarity



def recommend_movie(input_movie_name, df):
    input_movie = df[df['simpleTitle'] == input_movie_name]

    if input_movie.empty:
        print(f"No information found for the movie '{input_movie_name}'.")
        return None
    
    if len(input_movie) > 1:
        print(f'Be more specific. There is more than one movie with that title')
        return None
    
    input_cluster_label = input_movie['cluster'].values[0]
    
    features = mod.transform_features(df)
    
    #Features for input movie
    input_features = features[input_movie.index.values[0]].reshape(1, -1)
    
    #Calculate similarity based on Euclidean Distance
    cluster_movies = df[df['cluster'] == input_cluster_label]
    cluster_features = features[cluster_movies.index]
    
    similarities = np.sqrt(np.sum((cluster_features - input_features) ** 2, axis=1))
    top_similar_movies = df.loc[similarities.argsort()[1:4]] #to exclude the input movie
    top_similar_movies = top_similar_movies[['primaryTitle', 'genres']]
    
    return top_similar_movies
        
    
    

if __name__ == '__main__':
    df = pd.read_csv('movie_clusters.csv')
    
    input_movie = input("Enter the name of a holiday movie: ").strip().lower()
    similar_movies = recommend_movie(input_movie, df)
    
    print(f"\nTop 5 movies similar to '{input_movie}':")
    for index, row in similar_movies.iterrows():
        print(f"{row['primaryTitle']: <30} {row['genres']}")

    print("\n")