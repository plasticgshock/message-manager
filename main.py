from flask import Flask, request, render_template, redirect, url_for, jsonify
from datetime import datetime
import dbcrud
import requests
import json


def write_to_db(content, user_ip, user_agent):
    headers = {'Content-Type': 'application/json'}
    SERVER_URL = 'http://127.0.0.1:5002/api-access'
    
    # Create the request payload
    payload = json.dumps({'req':'create', 'data':content, 'ip':user_ip, 'agent': user_agent})
    
    # Send the POST request to the server
    response = requests.post(SERVER_URL, data=payload, headers=headers)
    
    if response.status_code == 200:
        # Parse the JSON response from the server
        status = response.json().get('response')
        print(f"Response from the server: {status}")
    else:
        print(f"Error:", response.json().get('error'))


app = Flask(__name__)


@app.route('/')
def index():
    return "hello world"


@app.route('/send', methods = ['POST', 'GET'])
def send():
    if request.method == "POST":
        message = request.form["ms"]
        data = {"content": message,
                "ip":request.remote_addr,
                "user_agent":request.headers.get("User-Agent")
                }
        print(data)
        write_to_db(data["content"], data["ip"], data["user_agent"])
        return redirect(url_for("send"))
    return render_template("sendmessage.html")


@app.route('/messages')
def DisplayMessages():
    headers = {'Content-Type': 'application/json'}
    SERVER_URL = 'http://127.0.0.1:5002/api-access'
    
    # Create the request payload
    payload = json.dumps({'req':'read'})
    
    # Send the POST request to the server
    response = requests.post(SERVER_URL, data=payload, headers=headers)
    
    if response.status_code == 200:
        # Parse the JSON response from the server
        messages = response.json().get('response')
        print(f"Response from the server: {messages}")
        reversed_messages = dict(reversed(list(messages.items())))
        return render_template('displaymessages.html', messages=reversed_messages)
    else:
        print(f"Error:", response.json().get('error'))
        return jsonify({'Error!':'error connecting to the db'})

if __name__ == '__main__':
    app.run(debug=True)
