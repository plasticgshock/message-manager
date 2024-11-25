from flask import Flask, request, render_template, redirect, url_for
import psycopg2 

app = Flask(__name__)

@app.route('/')
def index():
    return "hello world"

@app.route('/login', methods = ['POST', 'GET'])
def login():
    username = request.form["nm"]
    print(username)
    print({"ip":request.remote_addr})
    return render_template("login.html")

@app.route('/<usr>')
def user(usr):
    return f"<h1>{usr}, you've successfuly logged in!</h1>"

if __name__ == '__main__':
    app.run(debug=True)
