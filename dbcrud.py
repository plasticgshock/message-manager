import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from configparser import ConfigParser
from flask import Flask, jsonify, request


app = Flask(__name__)


def createtable():
    db_config = parse_db_config()
    try:
        connection = psycopg2.connect(**db_config)
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE requests (
                        request_id SERIAL PRIMARY KEY,
                        content TEXT NOT NULL, 
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
                        ip_address VARCHAR(45) NOT NULL, 
                        user_agent TEXT
                    );''')
        print("Table created")
    except (Exception, Error) as error:
        print(f"Error while creating table: {error}")        
    finally:
        cursor.close()
        connection.close()


def dbcheck():
    db_config = parse_db_config()
    db_config['database'] = 'postgres'
    try:
        connection = psycopg2.connect(**db_config)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        connection.autocommit = True
        cursor = connection.cursor()
        #check if db exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'messagemanager_db';")
        if not cursor.fetchone():
            # Create the database as it doesn't exist
            cursor.execute("CREATE DATABASE messagemanager_db;")
            print("Database 'messagemanager_db' created.")
            createtable()
        else:
            print("Database exists")
    except (Exception, Error) as error:
        return (f"Error while checking PostgreSQL database: {error}")
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("Database checked")


@app.route('/api-access', methods=['POST', 'GET'])
def process_request():
    dbcheck()
    if request.method == 'GET':
        return "dbcrud page"
    if request.json.get('req') == 'create':
        data = request.json.get('data')
        ip = request.json.get('ip')
        agent = request.json.get('agent')
        if data and ip and agent:
            response = write_messages(data, ip, agent)
            print(f"your data: {data}")
            return jsonify({'response': response})
        else:
            return jsonify({'error':'no data provided!'}), 400
    elif request.json.get('req') == 'read':
        return jsonify({'response':getmessages()})


def parse_db_config(filename='db_config.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    db_config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_config[param[0]] = param[1]
    else:
        raise Exception(f"Section {section} not found in the {filename} file")

    return db_config


def write_messages(data, ip, agent):
    try:
        db_config = parse_db_config()   # to be removed and rewritten so that the connection is always opened
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute(f'''INSERT INTO requests (content, ip_address, user_agent)
                       VALUES ('{data}', '{ip}', '{agent}' )''')
        connection.commit()
        return "successfully added data"
    except (Exception, Error) as error:
        return "Error while writing to PostgreSQL: "+error
    finally:
        if (connection):    # to be removed and rewritten so that the connection is always opened
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def getmessages():
    connection = None 
    try:
        params = parse_db_config()
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        cursor.execute('''SELECT * FROM requests ORDER BY timestamp DESC LIMIT 10;''')
        messages = cursor.fetchall()
        print("messages fetched")
        if len(messages)<10:
            l = len(messages)
        else:
                l = 10
        s = [0]*l
        dict0 = {}
        for i in range(l):
            dict0[messages[i][0]] = [messages[i][j] for j in range(1,5)]
        connection.commit()
        print("Successfully retrieved data")
        return dict(reversed(list(dict0.items())))
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


if __name__ == '__main__':
    app.run(debug=True, port=5002)
