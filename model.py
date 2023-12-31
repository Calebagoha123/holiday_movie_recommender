import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt

#Feature creation
def transform_features(data):
    enc = OneHotEncoder(handle_unknown='ignore')
    #scaler = StandardScaler()
    
    #OneHotEncode categorical variables
    #genres = data['genres'].str.get_dummies(sep=',').to_numpy() #each individual genre
    genres = enc.fit_transform(data[['genres']]).toarray() #each unique set of genres
    release_recency = (data['startYear'] >= 2000).astype(int).to_numpy().reshape(-1, 1)
    
    #Standardize continuous variables
    #average_rating = scaler.fit_transform(data[['averageRating']])
    #run_time = scaler.fit_transform(data[['runtimeMinutes']])

    #Convert continuous variables into categorical
    #rating = (data['averageRating'] >= 5).astype(int).to_numpy().reshape(-1, 1)
    #run_time = (data['runtimeMinutes'] >= 90).astype(int).to_numpy().reshape(-1, 1)
    
    #Add type of movie
    type_of_movie = data[['christmas', 'hanukkah', 'kwanzaa', 'holiday']].to_numpy()

    features = np.hstack((genres, type_of_movie, release_recency))
    return features

#Hyperparameter tuning to find optimal number of clusters
def optimize_model(features):
    highest_silhouette = 0
    best_model = ...
    
    for i in range(3, 10):
        model = AgglomerativeClustering(n_clusters=i, linkage='ward')
        labels = model.fit_predict(features)
        if silhouette_score(features, labels) > highest_silhouette:
            highest_silhouette = silhouette_score(features, labels) 
            best_model = model
    
    return highest_silhouette, best_model

if __name__ == '__main__':
    holiday_movies = pd.read_csv('holiday_movies.csv')
    holiday_movies = holiday_movies.dropna()

    features = transform_features(holiday_movies)
    
    
    #Build model
    silhouette, best_model = optimize_model(features)
    labels = best_model.fit_predict(features)
    print(silhouette)

    #Add cluster labels to dataframe
    holiday_movies['cluster'] = labels
    holiday_movies.to_csv('movie_clusters.csv', index='False')
    
    

    #Reduce dimensions for visualization
    #pca = PCA(n_components=2)
    #features_2d = pca.fit_transform(features)

    #Visualize clusters
    #plt.figure(figsize=(8, 6))
    #scatter = plt.scatter(features_2d[:, 0], features_2d[:, 1], c=labels, cmap='viridis')
    #plt.title('Hierarchical Clustering Visualization')
    #plt.xlabel('Principal Component 1')
    #plt.ylabel('Principal Component 2')
    #plt.legend(*scatter.legend_elements(), title='Clusters')
    #plt.show()

