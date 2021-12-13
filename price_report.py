import argparse
import random

import mysql.connector
import pandas as pd
from django.db import connection
from sqlalchemy import create_engine


def main(user, password, host='localhost', database='hbms'):
    try:
        connection = mysql.connector.connect(host=host,
                                             database=database,
                                             user=user,
                                             password=password)
        cursor = connection.cursor()

        print('For single rooms ...')
        for comb in [[0, 50], [50, 100], [100, 150], [150, 200], [200, 300], [300, 500], [500, 1000], [1000, 10000]]:
            command = """ SELECT hotel_id FROM room JOIN hotel on room.hotel_id = hotel.id WHERE num_people = 1 AND price BETWEEN %s AND %s GROUP BY hotel_id """
            cursor.execute(command, [comb[0], comb[1]])
            price_hotels = cursor.fetchall()
            num_hotels = len(price_hotels)

            command = """ SELECT COUNT(*), RIGHT(address, 2) FROM room JOIN hotel on room.hotel_id = hotel.id WHERE num_people = 1 AND price BETWEEN %s AND %s GROUP BY RIGHT(address, 2) """
            cursor.execute(command, [comb[0], comb[1]])
            num_rooms_by_state = cursor.fetchall()

            command = """ SELECT COUNT(hotel_id), RIGHT(address, 2) FROM hotel LEFT JOIN room on room.hotel_id = hotel.id WHERE room_no = 1 AND num_people = 1 AND price BETWEEN %s AND %s GROUP BY RIGHT(address, 2) """
            cursor.execute(command, [comb[0], comb[1]])
            num_hotels_by_state = cursor.fetchall()

            print('Price range in USD: ', comb)
            print('Number of hotels in this price range by state:', num_hotels_by_state)
            print('Number of rooms in this price range by state:', num_rooms_by_state)

        print('For double rooms ...')
        for comb in [[0, 50], [50, 100], [100, 150], [150, 200], [200, 300], [300, 500], [500, 1000], [1000, 10000]]:
            command = """ SELECT hotel_id FROM room JOIN hotel on room.hotel_id = hotel.id WHERE num_people = 2 AND price BETWEEN %s AND %s GROUP BY hotel_id """
            cursor.execute(command, [comb[0], comb[1]])
            price_hotels = cursor.fetchall()
            num_hotels = len(price_hotels)

            command = """ SELECT COUNT(*), RIGHT(address, 2) FROM room JOIN hotel on room.hotel_id = hotel.id WHERE num_people = 2 AND price BETWEEN %s AND %s GROUP BY RIGHT(address, 2) """
            cursor.execute(command, [comb[0], comb[1]])
            num_rooms_by_state = cursor.fetchall()

            command = """ SELECT COUNT(hotel_id), RIGHT(address, 2) FROM hotel LEFT JOIN room on room.hotel_id = hotel.id WHERE room_no = 1 AND num_people = 2 AND price BETWEEN %s AND %s GROUP BY RIGHT(address, 2) """
            cursor.execute(command, [comb[0], comb[1]])
            num_hotels_by_state = cursor.fetchall()

            print('Price range in USD: ', comb)
            print('Number of hotels in this price range by state:', num_hotels_by_state)
            print('Number of rooms in this price range by state:', num_rooms_by_state)

        for state in ['TX', 'PA', 'CA', 'NY', 'WA', 'FL', 'GA', 'VA', 'NC', 'SC', 'IL']:
            command = """ SELECT AVG(price) FROM room JOIN hotel on room.hotel_id = hotel.id WHERE num_people = 1 AND RIGHT(address, 2) = %s GROUP BY hotel_id """
            cursor.execute(command, [state])
            single_price = cursor.fetchall()[0]

            command = """ SELECT AVG(price) FROM room JOIN hotel on room.hotel_id = hotel.id WHERE num_people = 2 AND RIGHT(address, 2) = %s GROUP BY hotel_id """
            cursor.execute(command, [state])
            double_price = cursor.fetchall()[0]

            print(f'Average single room price for state {state} is {float(single_price[0])} USD')
            print(f'Average double room price for state {state} is {float(double_price[0])} USD')


    except mysql.connector.Error as error:
        print("Failed to execute: {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")



if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--host', type=str, default='localhost')
    parser.add_argument('--database', type=str, default='hbms')
    parser.add_argument('--user', type=str, required=True)
    parser.add_argument('--password', type=str, required=True)

    args = parser.parse_args()

    main(args.user, args.password, args.host, args.database)