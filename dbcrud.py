import psycopg2
from psycopg2 import Error
from configparser import ConfigParser
import datetime

# Given datetime object
def ManageDateOutput(dt:datetime):
    formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time



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


def insert(content:str, ip_address:str, user_agent:str):
    try:
        db_config = parse_db_config()
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute(f'''INSERT INTO requests (content, ip_address, user_agent)
                       VALUES ('{content}', '{ip_address}', '{user_agent}' )''')
        connection.commit()
        print("successfully added data")
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL:", error)
    finally:
        if (connection):
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
        s = [0]*10
        for i in range(10):
            s[i] = messages[i]
        connection.commit()
        print("Successfully retrieved data")
        return s

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


getmessages()