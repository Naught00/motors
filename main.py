from flask import Flask
from flask import render_template
from flask import g
from flask import  flash, request, redirect, url_for
from flask import send_from_directory, make_response
from flask import session
import os
import sqlite3
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/home/naught/prj/car/static/images/uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
DATABASE = 'cars.db'

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = ***REMOVED***

@app.route('/')
def index():
    con = get_db()
    cars = con.execute("SELECT * FROM cars")
    return render_template('index.html', cars=cars)

@app.route('/cars/<carid>')
def car(carid):
    con = get_db()

    cars = con.execute(f"SELECT * FROM cars WHERE car_id=?", carid)
    cars = cars.fetchall()

    pics = con.execute(f"SELECT * FROM pics WHERE id=?", carid)
    pics = pics.fetchall()

    return render_template('details.html', car=cars[0], pics=pics)

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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/portal', methods=['GET', 'POST'])
def portal():
    if 'password' not in session: 
        return "<p> no </p>"

    if request.method == 'POST':
        if 'files' not in request.files:
            return redirect(request.url)

        uploaded_files = request.files.getlist('files')

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if uploaded_files[0].filename == '':
            return redirect(request.url)

        for file in uploaded_files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                #return redirect(url_for('download_file', name=filename))


        title = request.form['title']
        price = int(request.form['price'])
        price = '{:,}'.format(price)
        print(price)
        text = request.form['text']
        print(type(text))
        print(text)
        # Use the first pic as thumbnail
        pic = secure_filename(uploaded_files[0].filename)
        print(pic)
        print(type(pic))

        print(title)
        db = get_db()
        db.execute("INSERT INTO cars (price, car_name, text, pics) VALUES(?, ?, ?, ?)", 
                   (price, title, text, pic))
        res = db.execute("SELECT MAX(car_id) from cars")
        res = res.fetchall()
        car_id = res[0][0]

        for file in uploaded_files:
            pic = secure_filename(file.filename)
            db.execute("INSERT INTO pics (id, pic) VALUES(?, ?)", 
                       (car_id, pic))
        db.commit()

        return redirect('/')

    db = get_db()
    cars = db.execute("SELECT * FROM cars")

    return render_template('portal.html', cars=cars)

@app.route('/delete', methods=['POST'])
def delete():
    car = request.form['name']
    car_id = request.form['id']

    print("DELETING:", car)

    db = get_db()
    db.execute("DELETE FROM cars WHERE car_name=?", (car,))
    db.execute("DELETE FROM pics WHERE id=?", (car_id,))
    db.commit()
    db.close()
    return redirect('/portal')
@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    if 'password' in session: 
        return redirect("/portal")

    if request.method == "POST":
        password = request.form['password']
        if password == "Tipperary88":
            session['password'] = password
            return redirect("/portal")

    return render_template('pass.html')

