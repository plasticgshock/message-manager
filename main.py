from flask import Flask, request, render_template, redirect, url_for, jsonify
import psycopg2 
from datetime import datetime
import dbcrud


def printdict(dict):
    for key in dict:
        print(f"{key} : {dict[key]}")


app = Flask(__name__)


@app.route('/')
def index():
    return "hello world"


@app.route('/send', methods = ['POST', 'GET'])
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
        dbcrud.insert(data["content"], data["ip"], data["user_agent"])
        return redirect(url_for("login"))
    return render_template("login.html")


@app.route('/messages')
def DisplayMessages():
    parsedMessages = dbcrud.getmessages()
    return jsonify(parsedMessages)

if __name__ == '__main__':
    app.run(debug=True)
