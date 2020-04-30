import configparser
import psycopg2
import time

config = configparser.ConfigParser()
config.read("config.ini")
USER = config["POSTGRES"]['user']
PASSWORD = config["POSTGRES"]['password']
HOST = config["POSTGRES"]['host']
PORT = config["POSTGRES"]['port']
DATABASE = config["POSTGRES"]['database']

connection = None
try:
    connection = psycopg2.connect(user=USER,
                                  password=PASSWORD,
                                  host=HOST,
                                  port=PORT,
                                  database=DATABASE)

    cursor = connection.cursor()
    # Print PostgreSQL Connection properties
    create_table_query = open("garden.sql", "r").read()
    cursor.execute(create_table_query)
except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)

finally:
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")


def tend():
    """Fetches sensor readings and adds them to the dbms"""
    pass

if __name__ == "__main__":
    while True:
        tend()              # collect data and record it
        time.sleep(60)      # wait 60 seconds for next recording
