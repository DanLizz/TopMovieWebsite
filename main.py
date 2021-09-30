from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

# Create Database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///top-movie-collection.db'
db = SQLAlchemy(app)


# Create Table
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(5000), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(1000), nullable=False)
    img_url = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        return f'<Movie {self.title}>'


db.create_all()

# Create Record
# new_movie = Movie(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's "
#                 "sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to "
#                 "a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )
#
# db.session.add(new_movie)
# db.session.commit()


# Home
@app.route("/", methods=["GET", "POST"])
def home():
    all_movies = db.session.query(Movie).all()
    return render_template("index.html", movies=all_movies)


# Edit Rating
@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        movie_id = request.form["id"]
        movie_to_update = Movie.query.get(movie_id)
        movie_to_update.rating = request.form["rating"]
        movie_to_update.review = request.form["review"]
        db.session.commit()
        return redirect(url_for('home'))
    movie_id = request.args.get('id')
    movie_selected = Movie.query.get(movie_id)
    return render_template("edit.html", movie=movie_selected)


# Delete Movie
@app.route("/delete", methods=["GET", "POST"])
def delete():
    movie_id = request.args.get('id')
    movie_to_delete = Movie.query.get(movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


# Add Movie
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_movie = Movie(title=request.form["title"])
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")


if __name__ == '__main__':
    app.run(debug=True)
