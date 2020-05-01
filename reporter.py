from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Response, make_response, \
    jsonify
from jinja2 import Environment
import flask
import os
import requests
import sqlite3
import threading
from PIL import Image, ExifTags
from contextlib import closing

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config['STATIC_FOLDER'] = os.getcwd()
cfg = None


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def connect_db():
    return sqlite3.connect('garden.db')


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def fetch_report():
    entries = {
        'time_stamp': [],
        'temperature': [],
        'humidity': [],
        'moistness': [],
        'image': []
               }
    headers = ['time_stamp','temperature','humidity','moistness','image']
    cur = g.db.execute("""
    SELECT *
    FROM garden""")
    for row in cur.fetchall():
        print(row, entries.keys())
        for key, element in zip(headers,row):
            entries[key].append(element)

    if request.headers.get('Accept') == "application/ld+json":  # if someone else is consuming
        return jsonify(entries)
    return render_template('dash.html', entries=entries)


if __name__ == '__main__':
   app.run(debug=True, port=80, host='0.0.0.0')
