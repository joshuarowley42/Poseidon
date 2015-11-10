from flask import Flask, app
from farm import Farm

farm = Farm()

app = Flask(__name__)

@app.before_request
def flask_before_req():
    farm.update()

from pages import views

