import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from database.models import db_drop_and_create_all, setup_db

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

    @app.route('/health')
    def health():
        return "This app is running :)"

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)