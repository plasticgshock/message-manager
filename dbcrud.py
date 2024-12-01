import psycopg2
from psycopg2 import Error


def insert(content:str, ip_address:str, user_agent:str):
    db_config = {"user":"postgres",
            "password":"6969",
            "host":"127.0.0.1",
            "port":"5432",
            "database":"messagemanager_db"}
    try:
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
