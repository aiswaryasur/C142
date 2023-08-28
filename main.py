from flask import Flask, jsonify, request
from demographic_filtering import output
from content_filtering import get_recommendations
import pandas as pd

movies_data = pd.read_csv('final.csv')

app = Flask(__name__)

all_movies = movies_data[["original_title","poster_link","release_date","runtime","weighted_rating"]]

liked_movies = []
not_liked_movies = []
did_not_watch = []

def assign_val():
    m_data = {
        "original_title": all_movies.iloc[0,0],
        "poster_link": all_movies.iloc[0,1],
        "release_date": all_movies.iloc[0,2] or "N/A",
        "duration": all_movies.iloc[0,3],
        "rating":all_movies.iloc[0,4]/2
    }
    return m_data

@app.route("/movies")
def get_movie():
    movie_data = assign_val()

    return jsonify({
        "data": movie_data,
        "status": "success"
    })

@app.route("/like")
def liked_movie():
    global all_movies
    movie_data=assign_val()
    liked_movies.append(movie_data)
    all_movies.drop([0], inplace=True)
    all_movies = all_movies.reset_index(drop=True)
    return jsonify({
        "status": "success"
    })

# api to return list of liked movies



@app.route("/dislike")
def unliked_movie():
    global all_movies

    movie_data=assign_val()
    not_liked_movies.append(movie_data)
    all_movies.drop([0], inplace=True)
    all_movies=all_movies.reset_index(drop=True)
    
    return jsonify({
        "status": "success"
    })

@app.route("/did_not_watch")
def did_not_watch_view():
    global all_movies

    movie_data=assign_val()
    did_not_watch.append(movie_data)
    all_movies.drop([0], inplace=True)
    all_movies=all_movies.reset_index(drop=True)
    
    return jsonify({
        "status": "success"
    })

# api to return list of popular movies
@app.route('/liked')
def liked():
    global liked_movies
    return jsonify({
        'data':liked_movies,
        'status':'success'
    })

@app.route('/popular_movies')
def popular_movies():
    popular_movies=[]
    for index,row in output.iterrows():
        p={
            'original_title':row['original_title'],
            'poster_link' :row['poster_link'],
            'release_date':row['release_date']or'N/A',
            'duration':row['runtime'],
            'rating':row['weighted_rating']/2
            
        } 
        popular_movies.append(p)
    return jsonify({
        'data':popular_movies,
        'status':'success'
    })

# api to return list of recommended movies
@app.route('/recommended_movies')
def recomended_movies():
    global liked_movies
    column_name=['original_title','poster_link','runtime','release_date','weighted_rating']
    all_recomended=pd.DataFrame(columns=column_name)

    for liked_movie in liked_movies:
        output=get_recommendations(liked_movie['original_title'])
        all_recomended=all_recomended.append(output)

    all_recomended.drop_duplicate(subset=['original_title'],inplace=True)
    recomended_movie=[]
    for index,row in all_recomended.iterrows():
        r={
           'original_title':row['original_title'],
            'poster_link' :row['poster_link'],
            'release_date':row['release_date']or'N/A',
            'duration':row['runtime'],
            'rating':row['weighted_rating']/2 
        }
        recomended_movie.append(r)
        return jsonify({
            'data':recomended_movie,
            'status':'success'

        })




if __name__ == "__main__":
  app.run()
