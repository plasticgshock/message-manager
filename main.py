from flask import Flask, request, render_template, redirect, url_for
import psycopg2 
from datetime import datetime

from dbcrud import insert


def printdict(dict):
    for key in dict:
        print(f"{key} : {dict[key]}")

app = Flask(__name__)

@app.route('/')
def index():
    return "hello world"

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == "POST":
        message = request.form["nm"]
        print(message)
        print(request.remote_addr)
        data = {"content": message,
                "ip":request.remote_addr,
                "user_agent":request.headers.get("User-Agent")
                }
        printdict(data)
        insert(data["content"], data["ip"], data["user_agent"])
        return redirect(url_for("login"))
    return render_template("login.html")

@app.route('/<usr>')
def user(usr):
    return f"<h1>{usr}, you've successfuly logged in!</h1>"

if __name__ == '__main__':
    app.run(debug=True)
