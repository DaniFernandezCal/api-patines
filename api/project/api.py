from flask import Flask
from flask_bcrypt import Bcrypt


app = Flask(__name__)
flask_bcrypt = Bcrypt(app)