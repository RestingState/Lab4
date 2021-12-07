from flask import Flask
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import sessionmaker
from src.database_model import engine

app = Flask(__name__)
app.testing = True
bcrypt = Bcrypt(app)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

from src.controller import api_blueprint
app.register_blueprint(api_blueprint)

if __name__ == '__main__':
    app.run(host='localhost', port='5000', debug=True)
