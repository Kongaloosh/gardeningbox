import Adafruit_DHT
from datetime import datetime
import os
import spidev  # To communicate with SPI devices
import sqlite3
import configparser
from contextlib import closing
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


def init_db():
    with closing(connect_db()) as db:
        with open('garden.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def connect_db():
    return sqlite3.connect("garden.db")


def tend():
    """Fetches sensor readings and adds them to the dbms"""
    moistness = read_moistness()
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    img_loc = None
    time_now = datetime.now()
    print(time_now, humidity, temperature, moistness)
    try:
        cursor = connect_db()
        print(cursor)
        postgres_insert_query = """
            INSERT INTO garden (time, humidity, temperature, soil_moisture, img_loc) 
            VALUES (?,?,?,?,?)"""
        record_to_insert = (time_now, humidity, temperature, moistness, img_loc)
        cursor.execute(postgres_insert_query, record_to_insert)
    except Exception as error:
        print("Error while connecting to PostgreSQL", error)


if __name__ == "__main__":
    while True:
        tend()  # collect data and record it
        time.sleep(60)  # wait 60 seconds for next recording
