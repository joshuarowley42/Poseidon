from flask import Flask, app
from farm import Farm

my_farm = Farm()

app = Flask(__name__)

@app.before_request
def flask_before_req():
    my_farm.update()

from pages import views

