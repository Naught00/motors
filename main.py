from flask import Flask
from flask import render_template
from flask import g
import sqlite3

DATABASE = 'cars.db'

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    con = get_db().cursor()
    cars = con.execute("SELECT * FROM cars")
    return render_template('index.html', cars=cars)

@app.route('/cars/<carid>')
def car(carid):
    con = get_db().cursor()
    car = con.execute(f"SELECT * FROM cars WHERE car_id={carid}")
    for car in car:
        return render_template('details.html', car=car)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
