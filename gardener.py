import Adafruit_DHT
import spidev  # To communicate with SPI devices
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

spi = spidev.SpiDev()  # Created an object
spi.open(0, 0)


def analog_input(channel):
    spi.max_speed_hz = 1350000
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data


def read_moistness(channel=0):
    temp = analog_input(channel)
    return (temp - 309.0) / (561.0 - 309.0)


connection = None
cursor = None
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
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")


def tend():
    """Fetches sensor readings and adds them to the dbms"""
    moistness = read_moistness()
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    img_loc = None

    try:
        connection = psycopg2.connect(user=USER,
                                      password=PASSWORD,
                                      host=HOST,
                                      port=PORT,
                                      database=DATABASE
                                      )



        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO garden (time, humidity, temperature, soil_moisture, img_loc) VALUES (%s,%s,%s,%s)"""
        record_to_insert = (time.time(), humidity, temperature, moistness, img_loc)
        cursor.execute(postgres_insert_query, record_to_insert)
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)


if __name__ == "__main__":
    while True:
        tend()  # collect data and record it
        time.sleep(60)  # wait 60 seconds for next recording
