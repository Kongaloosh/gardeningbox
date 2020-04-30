import configparser
import psycopg2

config = configparser.ConfigParser().read("config.ini")
USER = config["POSTGRES"]['user']
PASSWORD = config["POSTGRES"]['password']
HOST = config["POSTGRES"]['host']
PORT = config["POSTGRES"]['port']
DATABASE = config["POSTGRES"]['user']

try:
    connection = psycopg2.connect(user=USER,
                                  password=PASSWORD,
                                  host=HOST,
                                  port=PORT,
                                  database=DATABASE)

    cursor = connection.cursor()
    # Print PostgreSQL Connection properties
    print(connection.get_dsn_parameters(), "\n")

    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)

finally:
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")


