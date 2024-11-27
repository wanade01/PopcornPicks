from flask import Flask, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy, session
from flask.templating import render_template
from sqlalchemy import ForeignKey, create_engine, select
from dataclasses import dataclass
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
app.debug = True
CORS(app, resources={r"/add_user/*": {"origins": "http://localhost:4200"}})

#adds config for using a MySQL DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/popcornpicksdb'

#Creating an instance of SQLAlchemy
db = SQLAlchemy(app)

#Initializes flask-migrate
migrate = Migrate(app,db)

#Models
@dataclass
class Users(db.Model):
    user_id = db.Column(db.String(45), primary_key=True, unique=True, autoincrement=False)
    
@dataclass
class User_Info(db.Model):
    user_id = db.Column(db.String(45), ForeignKey(Users.user_id), primary_key=True, nullable=False)
    genre = db.Column(db.String(20), primary_key=True)
    
@dataclass
class User_Reviews(db.Model):
    user_id = db.Column(db.String(45), ForeignKey(Users.user_id), primary_key=True, nullable=False)
    movie_id = db.Column(db.Integer, primary_key=True)
    movie_rating = db.Column(db.Integer)
    movie_review = db.Column(db.String(10000))

@dataclass
class User_Watch_History(db.Model):
    user_id = db.Column(db.String(45), ForeignKey(Users.user_id), primary_key=True, nullable=False)
    movie_id = db.Column(db.Integer, primary_key=True)
    watch_date = db.Column(db.Date)
    favorite = db.Column(db.Boolean)

#Adds user based on the logged in user_id to db. If a user already exists, then
#a message is given that the user_id already exists.
@app.route('/add-user', methods=['POST'])
def add_user():
    print("Add User DB being accessed.")
    data = request.data
    userId = data.decode("utf-8")
    print("UserID is: " + userId)

    with app.app_context():
        q = db.session.query(Users).filter(
        Users.user_id==userId
        )

        if not userId:
            return jsonify({"error": "User ID is required"}), 400

        if(db.session.query(q.exists()).scalar()):
            return jsonify({"error": "User ID already exists"}), 400
        else:
            new_user = Users(user_id=userId)
            db.session.add(new_user)
            db.session.commit()
    
            print("Insert has been committed for UserID: " + userId)
    
            return jsonify({"status": "success", "userId": userId}), 200

#Adds rating for movie based on user_id and movie_id to db. If a rating already exists, then
#the rating gets updated.
@app.route('/add-rating', methods=['POST'])
def add_rating():
    print("Add Rating DB being accessed.")
    data = request.get_json()
    user_id = data.get('user_id')
    movie_id = data.get('movie_id')
    user_rating = data.get('movie_rating')
    
    
    with app.app_context():
        q = db.session.query(User_Reviews).filter(
            User_Reviews.user_id==user_id,
            User_Reviews.movie_id==movie_id
            )


        if(db.session.query(q.exists()).scalar()):
            db.session.query(User_Reviews).filter(
            User_Reviews.user_id==user_id,
            User_Reviews.movie_id==movie_id
            ).update({'movie_rating': user_rating})
            db.session.commit()
        else:
            new_entry = User_Reviews(user_id=user_id, movie_id = movie_id, movie_rating=user_rating)
            db.session.add(new_entry)
            db.session.commit()
    
    return jsonify({"status": "success", "movie_rating": user_rating}), 200

#Gets rating based on user_id and movie_id in User_Reviews table.
@app.route('/get-rating', methods=['POST'])
def get_rating():
    print("Get Rating DB being accessed.")
    data = request.get_json()
    user_id = data.get('user_id')
    movie_id = data.get('movie_id')
    
    with app.app_context():
        q = db.session.get(User_Reviews, (user_id, movie_id)).movie_rating
    
    return jsonify({"user_id": user_id, "movie_id": movie_id, "movie_rating": q}), 200

#Adds Review based on user_id and movie_id to db. If a review already exists, then
#the review gets updated.
@app.route('/add-review', methods=['POST'])
def add_review():
    print("Add Rating DB being accessed.")
    data = request.get_json()
    user_id = data.get('user_id')
    movie_id = data.get('movie_id')
    user_review = data.get('movie_review')
    
    with app.app_context():
        q = db.session.query(User_Reviews).filter(
            User_Reviews.user_id==user_id,
            User_Reviews.movie_id==movie_id
            )


        if(db.session.query(q.exists()).scalar()):
            db.session.query(User_Reviews).filter(
            User_Reviews.user_id==user_id,
            User_Reviews.movie_id==movie_id
            ).update({'movie_review': user_review})
            db.session.commit()
        else:
            new_entry = User_Reviews(user_id=user_id, movie_id = movie_id, movie_review=user_review)
            db.session.add(new_entry)
            db.session.commit()
    
    return jsonify({"status": "success", "movie_review": user_review}), 200

#Gets review based on user_id and movie_id in User_Reviews table.
@app.route('/get-review', methods=['POST'])
def get_review():
    print("Get Review DB being accessed.")
    data = request.get_json()
    user_id = data.get('user_id')
    movie_id = data.get('movie_id')
    
    with app.app_context():
        q = db.session.get(User_Reviews, (user_id, movie_id)).movie_review
    
    return jsonify({"user_id": user_id, "movie_id": movie_id, "movie_review": q}), 200

if __name__ == '__main__':
    app.run(debug=False)