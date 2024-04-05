# holiday_movie_recommender
'tis the season

# Data
I collected 1M+ rows of data from the IMDB database (see sources below) and filtered for all holiday movies. (See implementation in setup.py)
- holiday_movies.csv
- holiday_genres.csv

# Model
I applied one hot encoding to the genres column to get each unique set of genres and categorized the release year into recent or not recent (later than 2000). Finally, I added the type of movie and stacked all the features together into a feature matrix.

I then trained an Agglomerative Clustering (AC) algorithm using Ward linkage as it prioritizes minimizing the dissimiarity within clusters, which is important for recommending the most similar movies. I then implemented a function to find the most optimal number of clusters, evaluating on the silhouette score. 

I played around with different clustering algorithms (KMeans and DBSCAN) and found the best to be AC with about 9 clusters and a silhouette score of 0.35. Adding more features to the model such as average rating and run time decreased the performance.

I then assigned each movie to its cluster label and saved it to 'movie_clusters.csv'
(See implementation in model.py)

# Movie Recommender
From a holiday movie input, I find all other movies in its cluster and calculate the similarit based on Euclidean distance to find the top 3 similar movies.
(See implementation in recommend.py)

If you want to try it out for yourself, you can download this repo and run the recommend.py code. It will prompt you to input a holiday movie and return the 3 most similar movies for you to watch!

# Conclusion
This was just a fun little project I decided to attempt and familiarize myself with machine learning concepts I am currently learning. Any critique is very welcome. Contact me:
- Email: calebagoha@gmail.com
- LinkedIn: www.linkedin.com/in/caleb-agoha-262b28266



# Sources
https://datasets.imdbws.com/title.ratings.tsv.gz
https://datasets.imdbws.com/title.basics.tsv.gz
