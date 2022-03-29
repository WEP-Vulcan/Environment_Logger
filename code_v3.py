#!/usr/bin/env python3
import os
import sqlite3
import time
import datetime
import Adafruit_DHT
import RPi.GPIO as GPIO

DHT_SENSOR = Adafruit_DHT.AM2302
DHT_PIN = 22
REED_PIN = 11
FILENAME_PREFIX = 'Temp_Log-Location'
TIME_FORMAT = '%y-%m-%d_%H'

def get_db_filenames():
    time_now = datetime.datetime.now()
    time_now_str = time_now.strftime(TIME_FORMAT)
    filename = f'{FILENAME_PREFIX}-{time_now_str}'

    time_prev = time_now - datetime.timedelta(hours=1)
    time_prev_str = time_prev.strftime(TIME_FORMAT)
    filename_prev = f'{FILENAME_PREFIX}-{time_prev_str}'

    return filename_prev, filename


def create_db(filename):
    con = sqlite3.connect(filename)
    cur = con.cursor()

    cur.execute('''CREATE TABLE data (
        humidity REAL NOT NULL,
        temperature REAL NOT NULL,
        door_state TEXT NOT NULL,
        recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')

    con.commit()
    con.close()


def manage_dbs(filename_prev, filename):
    if not os.path.exists(filename):
        create_db(filename)
    
    if os.path.exists(filename_prev):
        # upload the file somehow

        # delete the file
        os.remove(filename_prev)


def write_to_db(filename, humidity, temperature, state):
    print(f'Humidity: {humidity:0.1f}%  Temp: {temperature:0.1f}*C  Door State: {state}')

    con = sqlite3.connect(filename)
    cur = con.cursor()

    cur.execute('''INSERT INTO data
        (humidity, temperature, door_state)
        VALUES (?, ?, ?)''', (humidity, temperature, state))

    con.commit()
    con.close()


def read_data(filename):
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

    if humidity is None or temperature is None:
        print('Failed Reading DHT22')
        return

    humidity = round(humidity, 3)
    temperature = round(temperature, 3)
    sleep_for = 60

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(REED_PIN, GPIO.IN)

    #If door sensor is closed do this
    if GPIO.input(REED_PIN):
        state = 'Closed'

    #If door sensor is open do this
    else:
        state = 'Open'
        sleep_for = 5

    write_to_db(filename, humidity, temperature, state)
    time.sleep(sleep_for)


if __name__ == '__main__':
    try:
        #Activate loop
        while True:
            print('Program Running')
            filename_prev, filename = get_db_filenames()

            manage_dbs(filename_prev, filename)
            read_data(filename)

    #When prog cancelled return to normal state
    except KeyboardInterrupt: 
        GPIO.cleanup()
