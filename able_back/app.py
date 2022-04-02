from gc import collect
from flask.helpers import make_response
import json
import os
from bibles import Bibles
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')

@app.route('/book_list')
def book_list():
    #make this path settable
    collection = Bibles("./.sword")
    versions = collection.get_versions()
    #make default book, version settable
    version = "DRC"
    if "version" in request.args:
        if request.args["version"] in versions.keys():
            version = request.args["version"] 
    return json.dumps(collection.get_books(version))

@app.route('/text')
def get_text():
    collection = Bibles("./.sword")
    versions = collection.get_versions()
    #make default book, version settable
    version = "DRC"
    book = "john"
    verses = None
    chapter = 3
    if "version" in request.args:
        if request.args["version"] in versions.keys():
            version = request.args["version"]
    if "book" in request.args:
        book = request.args["book"]
    if "end" in request.args:
        if "start" in request.args:
            verses = [int(request.args["start"]),int(request.args["end"])]
        else:
            verses = [1, int(request.args["end"])]
    if "chapter" in request.args:
        chapter = [int(request.args["chapter"])]
    return json.dumps(collection.get_text(version,book, chapters=chapter, verses = verses))

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)