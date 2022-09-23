import json
from urllib import response
from urllib.request import parse_keqv_list
from flask import Flask, render_template
from flask import request

import requests

app = Flask(__name__)

# server url used for the data stored in a db
BACKEND_URL = "http://127.0.0.1:5000/notes"

# recives data


@app.get("/")
def get_index():
    response = requests.get(BACKEND_URL)
    scan_data = response.json()
    return render_template("main.html", notes=scan_data)  # render the page

# About page were there is data from the creator of the page


@app.get("/about")
def about():
    me = {
        "first_name": "Sebastian",
        "last_name": "Lopez-Wells",
        "hobbies": "Baseball, Programming",
        "bio": "Student on ITT and SDGKU."
    }
    return render_template('about.html', about_dict=me)


@app.get("/yourNotes")
def get_list():
    response = requests.get(BACKEND_URL)
    scan_data = response.json()
    return render_template("list.html", notes=scan_data)


@app.get("/change/notes/<int:pk>")
def modify_notes(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    response = requests.get(url)
    note = response.json()
    return render_template("update.html", note=note[0])


@app.post("/modify/notes/<int:pk>")
def update_notes(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    form_data = request.form
    new_dt = {
        "title": form_data.get("title"),
        "subtitle": form_data.get("subtitle"),
        "body": form_data.get("body"),
    }
    response = requests.put(url, json=new_dt)

    if response.status_code == 204:
        return render_template("new_success.html")
    else:
        return render_template("failed.html")


@app.get("/create/note")
def add_notes():
    return render_template("add.html")


@app.get("/erase/note/<int:pk>")
def deletes_notes(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    response = requests.get(url)
    note = response.json()
    return render_template("delete.html", note=note[0])


@app.post("/delete/notes/<int:pk>")
def delete_notes(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    response = requests.delete(url)

    if response.status_code == 204:
        return render_template("new_success.html")
    else:
        return render_template("failed.html")


@app.post("/create/note")
def create_notes():
    form_data = request.form
    new_dt = {
        "title": form_data.get("title"),
        "subtitle": form_data.get("subtitle"),
        "body": form_data.get("body")
    }
    response = requests.post(BACKEND_URL, json=new_dt)

    if response.status_code == 204:
        return render_template("new_success.html")
    else:
        return render_template("failed.html")
