NJ motors website

# Run

    $ pip install -r requirements.txt

Initialsise the database:

    $ touch cars.db
    $ sqlite3 cars.db < schema.sql

Set the secret key to be used for message flashing:

    $ export CAR_SECRET_KEY=<key>

Set the directory to be used for user image uploads:

    $ export UPLOADS_DIRECTORY=/path/to/directory

Start uwsgi:
    
    $ uwsgi --socket 127.0.0.1:3031 --wsgi-file main.py --callable app --master --processes 10 --threads 10 --stats 127.0.0.1:9191

Configure nginx to be used as a reverse proxy that points to the uwsgi process:

    	location / {
	    include uwsgi_params;
	    uwsgi_pass 127.0.0.1:3031;
	}






