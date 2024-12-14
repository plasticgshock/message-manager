from flask import Flask, request, render_template, redirect, url_for, jsonify
from datetime import datetime
import dbcrud
import requests
import json


def write_to_db(content, user_ip, user_agent):
    headers = {'Content-Type': 'application/json'}
    SERVER_URL = 'http://127.0.0.1:5002/api-access'
    
    # Create the request payload
    payload = json.dumps({'data':content, 'ip':user_ip, 'agent': user_agent})
    
    # Send the POST request to the server
    response = requests.post(SERVER_URL, data=payload, headers=headers)
    
    if response.status_code == 200:
        # Parse the JSON response from the server
        status = response.json().get('response')
        print(f"Response from the server: {status}")
    else:
        print(f"Error:", response.json().get('error'))

def printdict(dict):
    for key in dict:
        print(f"{key} : {dict[key]}")


app = Flask(__name__)


@app.route('/')
def index():
    return "hello world"


@app.route('/send', methods = ['POST', 'GET'])
def send():
    if request.method == "POST":
        SERVER_URL = 'http://127.0.0.1:5000/api-access'
        message = request.form["nm"]
        data = {"content": message,
                "ip":request.remote_addr,
                "user_agent":request.headers.get("User-Agent")
                }
        printdict(data)
        print(data)
        write_to_db(data["content"], data["ip"], data["user_agent"])
        return redirect(url_for("send"))
    return render_template("login.html")


@app.route('/messages')
def DisplayMessages():
    parsedMessages = dbcrud.getmessages()
    return jsonify(parsedMessages)

if __name__ == '__main__':
    app.run(debug=True)
