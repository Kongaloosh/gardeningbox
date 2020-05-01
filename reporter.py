from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Response, make_response, \
    jsonify
from jinja2 import Environment
import flask
import psycopg2
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
    return sqlite3.connect(app.config['DATABASE'])


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
    entries = []
    cur = g.db.execute("""
    SELECT *
    FROM garden
    ORDER BY garden.time DESC""")
    for (row,) in cur.fetchall():
        entries.append(row)
        if len(entries) >= 20:
            break
    return render_template('dash.html', entries)