import psycopg2

try:
    connection = psycopg2.connect(user="postgres",
                  password="6969",
                  host = "127.0.0.1",
                  database="messagemanager_db")

    cursor = connection.cursor()
    print("Psycopg2 server information: ")
    print(connection.get_dsn_parameters(), "\n")
    cursor.execute("SELECT VERSION();")
    record = cursor.fetchone

    print("You are connected to ", record, "\n")
except Exception as error:
    print("Error while connecting to the db PostgreSQL", error)

finally:
    if (connection):
        cursor.close()
        connection.close()
        print("Postgresql connection is closed")