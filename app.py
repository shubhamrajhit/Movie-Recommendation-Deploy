from flask import Flask ,render_template,request
import pickle
import numpy as np
import pandas as pd
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity



data=pd.read_csv('movie_dataset_github.csv')


app=Flask(__name__)

cvr=pickle.load(open("cvr.pkl","rb"))
count_matrix=pickle.load(open('count_matrix.pkl','rb'))
cosine_similarity=pickle.load(open('cosine_similarity.pkl','rb'))

def get_title_from_index(index):
    return data[data['index'] == index]['title'].values[0]
def get_index_from_movie_title(title):
    return data[data['title'] == title ]['index'].values[0]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    similarMovies= [ ]
    error=" "
    i=0
    try:
        movie_user_likes = request.form.get('movie')
        movie_index = get_index_from_movie_title(movie_user_likes)
        similar_movies = list(enumerate(cosine_similarity[movie_index]))
        sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[1:]
        for element in sorted_similar_movies:
            similarMovies.append(get_title_from_index(element[0]))
            i = i + 1
            if i > 5:
                break
        return render_template('index.html',similar_movies=similarMovies)
    except:
        return render_template('index.html',error="please input the appropriate name" )


if __name__=="__main__":
    app.run(debug=True)
