import json
import os
import sys
from urllib.parse import quote_plus, urlencode
from dotenv import find_dotenv, load_dotenv
from flask import Flask, flash, redirect, render_template, request, abort, jsonify, session, url_for
from flask_cors import CORS
from auth import AuthError, requires_auth
from database.models import db, Actor, Movie, db_drop_and_create_all, setup_db
from forms import ActorForm, MovieForm

from authlib.integrations.flask_client import OAuth

SECRET_KEY = os.urandom(32)


def create_app(db_URI="", test_config=None):
  # create and configure the app
  app = Flask(__name__)
  
  if db_URI:
    setup_db(app, db_URI)
  else:
    setup_db(app)  

    """
    Uncomment these to reset the database
    NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
    """
    with app.app_context():
       db_drop_and_create_all()
       
    CORS(app)

    app.config['SECRET_KEY'] = SECRET_KEY
    

    ENV_FILE = find_dotenv()
    if ENV_FILE:
        load_dotenv(ENV_FILE)

    oauth = OAuth(app)

    oauth.register(
    "auth0",
    client_id=os.environ.get("AUTH0_CLIENT_ID"),
    client_secret=os.environ.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{os.environ.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
    )

    @app.route("/login")
    def login():   
        return oauth.auth0.authorize_redirect(
            redirect_uri=url_for("callback", _external=True)
        )
    
    @app.route("/callback", methods=["GET", "POST"])
    def callback():
        token = oauth.auth0.authorize_access_token()
        session["user"] = token
        return redirect("/")


#  -------------------------------------------------------------------------#
#  Controllers
#  -------------------------------------------------------------------------#
    
    # health check
    @app.route('/health')
    def health():
        return "This app is running :)"
    
    # homepage
    @app.route('/')
    def index():
      return render_template('pages/home.html', session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(
            "https://" + os.environ.get("AUTH0_DOMAIN")
            + "/v2/logout?"
            + urlencode(
                {
                    "returnTo": url_for("home", _external=True),
                    "client_id": os.environ.get("AUTH0_CLIENT_ID"),
                },
                quote_via=quote_plus,
            )
        )

#  -------------------------------------------------------------------------#
#  Actors
#  -------------------------------------------------------------------------#    
    
    # get all Actors
    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors():
        actors = Actor.query.order_by(Actor.id).all()
        formatted_actors = [actor.format() for actor in actors]

        return render_template('pages/actors.html', actors=formatted_actors)

    # Actor Form 
    @app.route('/actors/create', methods=['GET'], endpoint='new_actor')
    @requires_auth('get:actors')
    def create_actor_form():
     form = ActorForm()
     return render_template('forms/new_actor.html', form=form)
    
    # Create Actor
    @app.route('/actors/create', methods=['POST']) 
    @requires_auth('post:actors')
    def create_actor_submission():
      form = ActorForm()
      error = False
      try:
          actor = Actor(          
            name=form.name.data,
            age=form.age.data,
            gender=form.gender.data)


          db.session.add(actor)
          db.session.commit()
      except:
          error = True
          db.session.rollback()
          print(sys.exc_info())
      finally:
          
          db.session.close()
          if error:
              flash('An error occured. Actor ' + request.form['name'] + ' Could not be listed!')
          else:
              flash('Actor ' + request.form['name'] + ' was successfully listed!')

      return render_template('pages/home.html')
    
    # show Actor
    @app.route('/actors/<int:actor_id>')
    def show_actor(actor_id):
        actor = Actor.query.get(actor_id)
       
        
        return render_template('pages/actor.html', actor=actor)
    
    # Update Actor
    @app.route('/actors/<int:actor_id>/edit', methods=['GET'])
    @requires_auth('patch:actors')
    def edit_actor(actor_id):
        form = ActorForm()

        actor = Actor.query.get(actor_id)

        # Pre populates fields so the user doesnt have to type everything again, they can just make edits
        form.name.data = actor.name
        form.age.data = actor.age
        form.gender.data = actor.gender

        return render_template('forms/edit_actor.html', form=form, actor=actor)
    
    @app.route('/actors/<int:actor_id>/edit', methods=['POST'])
    @requires_auth('patch:actors')
    def edit_actor_submission(actor_id):
        form = ActorForm()
        try:

            actor = Actor.query.get(actor_id)

            # Replaces the orignal data with the updated form data
            actor.name = form.name.data
            actor.age = form.age.data
            actor.gender = form.gender.data


            db.session.commit()
            flash( request.form['name'] + ' was successfully updated!')

        except Exception as e:
            db.session.rollback()
            flash('An error occurred.' + request.form['name'] + ' could not be updated.')

        finally:
            db.session.close()

        return redirect(url_for('show_actor', actor_id=actor_id))

    # Delete Actor
    @app.route('/actors/<actor_id>/delete', methods=['GET'])
    @requires_auth('delete:movies')
    def delete_actor(actor_id):   
        error = False
        try:
            Actor.query.filter_by(id=actor_id).delete()
            db.session.commit()
        except:
            error = True
            db.session.rollback()
        finally:
            db.session.close()
            if error:
                flash('Actor could not be deleted. Please try again later')
            else:
                flash('Actor Succesfully deleted')
        return render_template('pages/home.html')



#  -------------------------------------------------------------------------#
#  Movies
#  -------------------------------------------------------------------------#
    
    # get all movies
    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies():
        movies = Movie.query.order_by(Movie.id).all()
        formatted_movies = [movie.format() for movie in movies]

        return render_template('pages/movies.html', movies=formatted_movies)
    
    # Movie Form
    @app.route('/movies/create', methods=['GET'], endpoint='new_movie')
    @requires_auth('post:movies')
    def create_movie_form():
     form = MovieForm()
     return render_template('forms/new_movie.html', form=form)
    
    # Create Movie
    @app.route('/movies/create', methods=[ 'POST']) 
    @requires_auth('post:movies')
    def create_movie_submission():
      form = MovieForm()
      error = False
      try:
          movie = Movie(          
            title=form.title.data,
            release_date=form.release_date.data)


          db.session.add(movie)
          db.session.commit()
      except:
          error = True
          db.session.rollback()
          print(sys.exc_info())
      finally:
          
          db.session.close()
          if error:
              flash('An error occured. The Movie ' + request.form['name'] + ' Could not be listed!')
          else:
              flash('Movie' + request.form['name'] + ' was successfully listed!')

      return render_template('pages/home.html')

    # show Movie
    @app.route('/movies/<int:movie_id>')
    def show_movie(movie_id):
        movie = Movie.query.get(movie_id)
       
        
        return render_template('pages/movie.html', movie=movie)
    
    # Update Movie
    @app.route('/movies/<int:movie_id>/edit', methods=['GET'])
    @requires_auth('get:movies')
    def edit_movie(movie_id):
        form = MovieForm()

        movie = Movie.query.get(movie_id)

        # Pre populates fields so the user doesnt have to type everything again, they can just make edits
        form.title.data = movie.title
        form.release_date.data = movie.release_date

        return render_template('forms/edit_movie.html', form=form, movie=movie)
    
    @app.route('/movies/<int:movie_id>/edit', methods=['POST'])
    @requires_auth('patch:movies')
    def edit_movie_submission(movie_id):
        form = MovieForm()
        try:

            movie = Movie.query.get(movie_id)

            # Replaces the orignal data with the updated form data
            movie.title = form.title.data
            movie.release_date = form.release_date.data

            db.session.commit()
            flash( request.form['title'] + ' was successfully updated!')

        except Exception as e:
            db.session.rollback()
            flash('An error occurred.' + request.form['title'] + ' could not be updated.')

        finally:
            db.session.close()

        return redirect(url_for('show_movie', movie_id=movie_id))

    # Delete Movie
    @app.route('/movies/<movie_id>/delete', methods=['GET'])
    @requires_auth('delete:movies')
    def delete_movie(movie_id):   
        error = False
        try:
            Movie.query.filter_by(id=movie_id).delete()
            db.session.commit()
        except:
            error = True
            db.session.rollback()
        finally:
            db.session.close()
            if error:
                flash('Movie could not be deleted. Please try again later')
            else:
                flash('Movie Succesfully deleted')
        return render_template('pages/home.html')


#  -------------------------------------------------------------------------#
#  Errors
#  -------------------------------------------------------------------------#

    """Error handlers for expected errors"""
    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({
                "success": False,
                "error": 400,
                "message": "bad request"
            }), 400)

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({
                "success": False,
                "error": 404,
                "message": "resource not found"
            }), 404)

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (
            jsonify({
                "success": False,
                "error": 405,
                "message": "method not allowed"
            }), 405)

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({
                "success": False,
                "error": 422,
                "message": "unprocessable"
            }), 422)

    @app.errorhandler(500)
    def unprocessable(error):
        return (
            jsonify({
                "success": False,
                "error": 500,
                "message": "internal server error"
            }), 500)
    
  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)