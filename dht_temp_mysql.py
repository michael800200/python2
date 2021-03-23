# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_dht
import pymysql.cursors

# 訊號腳位 GPIO 26 >>>不懂import board但為什麼是看GPIO的腳位
dhtDevice = adafruit_dht.DHT22(board.D26)

# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
# dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)

while 1==1:
    try:
        connection = pymysql.connect(host='192.168.137.1',
                             user='pi',
                             password='aiot08',
                             database='no18',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        t = time.localtime()
        now = time.strftime("%Y-%m-%d %H:%M:%S", t)
        with connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `senser` (`temperature`, `humidity`, `time`) VALUES (%s, %s, %s)"
                cursor.execute(sql, (temperature_c, humidity, now))
                print(humidity)
                print(temperature_c)
                print(now)
            connection.commit()
        print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                temperature_f, temperature_c, humidity
            )
        
        )
        
        

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(2.0)
    
