from flask import Flask
import os

app = Flask(__name__, static_url_path='/static')

app.secret_key = 'Vive_Patrice_<3' # À CHANGER QUAND PASSAGE EN PROD

from app.controllers import *