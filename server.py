from flask import (Flask, render_template, request, flash, session,redirect)

from model import connect_to_db, db
from jinja2 import StrictUndefined
import crud
app = Flask(__name__)

app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():

    return render_template('homepage.html')

@app.route("/movies")
def all_movies():

    movies = crud.get_movies()

    return render_template("all_movies.html", movies=movies)

@app.route("/users")
def all_users():

    users = crud.get_users()

    return render_template("all_users.html", users=users)

@app.route("/movies/<movie_id>")
def show_movie(movie_id):
    movie = crud.get_movie_by_id(movie_id)

    return render_template("movie_details.html", movie=movie)

@app.route("/users", methods=["POST"])
def register_user():

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")

@app.route("/login", methods=["POST"])
def process_login():

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")

    return redirect("/")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="localhost",port = 5000, debug=True)