"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    a = jsonify([1,3])
    return render_template("homepage.html")


@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.order_by(User.user_id)
    return render_template("user_list.html", users=users)


@app.route("/users/<user_id>")
def user_details(user_id):
    """Show user details."""

    user = User.query.filter_by(user_id=user_id).one()
    return render_template("user_info.html", user=user)


@app.route("/movies")
def movie_list():movie_info = Mo
    """Show a listing of movies."""

    movies = Movie.query.order_by(Movie.title)
    return render_template("movie_list.html", movies=movies)


@app.route("/movies/<movie_id>")
def movie_details(movie_id):
    """Show user details."""

    movie = Movie.query.filter_by(movie_id=movie_id).one()
    session['current_movie'] = movie_id
    return render_template("movie_info.html", movie=movie)


@app.route('/register', methods=["GET"])
def register_form():

    return render_template("register_form.html")


@app.route('/register', methods=["POST"])
def register_process():

    email = request.form.get("email")
    password = request.form.get("password")
    age = request.form.get("age")
    zipcode = request.form.get("zipcode")

    db_email = User.query.filter_by(email=email).all()

    if not db_email:
        user = User(
            email=email,
            password=password,
            age=age,
            zipcode=zipcode)

        db.session.add(user)
        db.session.commit()
        flash("Account successfully created.")
        return redirect("/")
    else:
        flash("This email already exists. Try again.")
        return redirect("/register")


@app.route('/rate/<movie_id>')
def rate_form(movie_id):
    movie_id = session['current_movie']
    movie = Movie.query.filter_by(movie_id=movie_id).one()
    return render_template("rate_form.html", movie=movie)


@app.route('/rate', methods=["POST"])
def rate_process():

    movie = session["current_movie"]
    score = request.form.get("rating")
    user = session["current_user"]
    movie_info = Movie.query.filter_by(movie_id=movie_id).one()
    pass

@app.route('/login', methods=["GET"])
def login_form():

    return render_template("login_form.html")


@app.route('/login', methods=["POST"])
def login_process():

    email = request.form.get("email")
    password = request.form.get("password")

    db_login = User.query.filter_by(email=email).first()
    #validate login information
    if not db_login or db_login.password != password:
        flash("Email or Password do not match, please try again.")
        return redirect("/login")
    else:
        session['current_user'] = email
        flash("Welcome Back {}!".format(email))
        return redirect("/users/" + str(db_login.user_id))


@app.route('/logout')  # methods=["POST"]
def logout_process():

    del session['current_user']
    flash("Goodbye! You have successfully logged out.")
    return redirect("/")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)



    # app.run(port=5000, host='0.0.0.0')
