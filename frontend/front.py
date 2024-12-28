from flask import Flask, request, render_template, redirect, url_for, jsonify
import requests
import json
import os

BACKEND_URL = 'http://backend:5002' # имя контейнера в докере

def write_to_db(content, user_ip, user_agent):
    headers = {'Content-Type': 'application/json'}
    SERVER_URL = f'{BACKEND_URL}/api/v1/postMessage'
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
def test():
    SERVER_URL = f'{BACKEND_URL}/api/v1/getMessages'
    response = requests.get(SERVER_URL)
    if response.status_code == 200:     
        data = response.json()
        return render_template('displaymessages.html', messages=data)
    else:
        return "ERROR: Database unreachable"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)