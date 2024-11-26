from flask import Flask, request, jsonify, render_template, request
from flask_cors import CORS, cross_origin
import os
import requests
import sys
import sqlalchemy
from dotenv import load_dotenv
from flask_mysqldb import MySQL
from app import Users,User_Info,User_Reviews,User_Watch_History,add_user

load_dotenv()
TMDB_API_KEY = os.getenv('TMDB_API_KEY')

search = Flask(__name__)
CORS(search, resources={r"/search/*": {"origins": "http://localhost:4200"}}) 
CORS(search, resources={r"/movie/*": {"origins": "http://localhost:4200"}})


search.app_context()
@search.route('/search', methods=['GET'])
def search_movies():
    query = request.args.get('query')
    response = requests.get(f'https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}')
    return jsonify(response.json())

@search.route('/movie', methods=['GET'])
def getMovie():
    movie_id = request.args.get('id')
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}')
    print(response.text)
    return jsonify(response.json())

@search.route('/addUser', methods=['POST', 'OPTIONS'])
def addUser():
    print("Add user being accessed")
    response = add_user()
    print(response)
    return 42

if __name__ == '__main__':
    search.run(debug=False)