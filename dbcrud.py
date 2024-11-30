import psycopg2
from psycopg2 import Error

try:
    # Connect to an existing database
    connection = psycopg2.connect(user="postgres",
                                  password="6969",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="messagemanager_db")

    # Create a cursor to perform database operations
    cursor = connection.cursor()
    # Print PostgreSQL details
    print("PostgreSQL server information")
    print(connection.get_dsn_parameters(), "\n\n\n")
    # Executing a SQL query
    cursor.execute('''INSERT INTO requests (content, ip_address, user_agent) VALUES ('Hello postgres', '10.10.155.168', 'Firefox')''')

    cursor.execute('''SELECT * FROM requests;''')
    contents = cursor.fetchall()
    print(contents)

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")