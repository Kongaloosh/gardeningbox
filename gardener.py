import Adafruit_DHT
import configparser
from contextlib import closing
from cv2 import *
from datetime import datetime
import os
import spidev  # To communicate with SPI devices
import sqlite3
import time

spi = spidev.SpiDev()
spi.open(0, 0)

cam = VideoCapture(0)

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
    s, img = cam.read()
    if s:
        img_loc = "images/{0}.jpg".format(time_now.strftime("%Y-%m-%d-%H-%M-%S"))
        imwrite(img_loc,img)

    try:
        cursor = connect_db()
        postgres_insert_query = """
            INSERT INTO garden (time, humidity, temperature, soil_moisture, img_loc) 
            VALUES (?,?,?,?,?)"""
        record_to_insert = [time_now, humidity, temperature, moistness, img_loc]
        cursor.execute(postgres_insert_query, record_to_insert)
        cursor.commit()
    except Exception as error:
        print(error)


if __name__ == "__main__":
    while True:
        tend()  # collect data and record it
        time.sleep(60)  # wait 60 seconds for next recording
