import argparse
import random

import mysql.connector
import pandas as pd
from django.db import connection
from sqlalchemy import create_engine


def main(user, password, host='localhost', database='hbms'):
    try:
        connection = mysql.connector.connect(host=host,
                                             # database=database,
                                             user=user,
                                             password=password)
        cursor = connection.cursor()

        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        # cursor.execute(f"GRANT ALL ON {database}.* TO {user}@{host}")
        connection.database = database

        engine = create_engine(f"mysql://{user}:{password}@{host}/{database}")
        con = engine.connect()

        create_hotel_table_command = """ CREATE TABLE hotel
                                        (
                                          id              INT unsigned NOT NULL AUTO_INCREMENT,
                                          name            VARCHAR(150) NOT NULL,
                                          address         VARCHAR(150) NOT NULL,
                                          zip_code        VARCHAR(10),
                                          phone           VARCHAR(15),
                                          web_url         VARCHAR(500),
                                          rating          FLOAT,
                                          num_review      INT unsigned,
                                          manager_id      BIGINT DEFAULT 2,
                                          FOREIGN KEY     (manager_id) REFERENCES users_user(id),
                                          PRIMARY KEY     (id)
                                        ); 
                                     """
        delete_hotel_table_command = """ DROP TABLE hotel; """
        delete_room_table_command = """ DROP TABLE room; """
        delete_reservation_table_command = """ DROP TABLE reservation; """
        delete_reserved_room_table_command = """ DROP TABLE reserved_room; """

        create_room_table_command = """ CREATE TABLE room
                                        (
                                          id              INT unsigned NOT NULL AUTO_INCREMENT,
                                          room_no         INT unsigned NOT NULL,
                                          num_people      INT unsigned NOT NULL,
                                          price           INT unsigned NOT NULL,
                                          hotel_id        INT unsigned NOT NULL,
                                          FOREIGN KEY     (hotel_id) REFERENCES hotel(id),
                                          PRIMARY KEY     (id)
                                        ); 
                                     """

        create_reservation_table_command = """ CREATE TABLE reservation
                                              (
                                                id              INT unsigned NOT NULL AUTO_INCREMENT,
                                                res_date        DATE NOT NULL,
                                                start_date      DATE NOT NULL,
                                                end_date        DATE NOT NULL,
                                                customer_id     BIGINT NOT NULL,
                                                hotel_id        INT unsigned NOT NULL,
                                                price           INT unsigned NOT NULL,
                                                rating          SMALLINT,
                                                FOREIGN KEY     (customer_id) REFERENCES users_user(id),
                                                FOREIGN KEY     (hotel_id) REFERENCES hotel(id),
                                                PRIMARY KEY     (id)
                                              ); 
                                           """

        create_reserved_room_table_command = """ CREATE TABLE reserved_room
                                                (
                                                  id              INT unsigned NOT NULL AUTO_INCREMENT,
                                                  res_id          INT unsigned NOT NULL,
                                                  room_id         INT unsigned NOT NULL,
                                                  FOREIGN KEY     (res_id) REFERENCES reservation(id) ON DELETE CASCADE,
                                                  FOREIGN KEY     (room_id) REFERENCES room(id) ON DELETE CASCADE,
                                                  PRIMARY KEY     (id)
                                                ); 
                                             """

        # cursor.execute(delete_reserved_room_table_command)
        # cursor.execute(delete_reservation_table_command)
        # cursor.execute(delete_room_table_command)
        # cursor.execute(delete_hotel_table_command)

        cursor.execute(create_hotel_table_command)
        df = pd.read_csv('data/findhotel/formatted_data.csv')
        df = df[~df.name.isnull()]
        prices = df.price
        df.drop('price', axis=1, inplace=True)
        df.to_sql(con=con, name='hotel', index=False, index_label='id', if_exists='append')  # performs INSERT

        cursor.execute(create_room_table_command)
        cursor.execute(create_reservation_table_command)
        cursor.execute(create_reserved_room_table_command)

        fill_rooms = True
        if fill_rooms:
            for hotel_id in range(1, len(df)+1):
                price_2 = int(prices[hotel_id-1].replace(',', ''))
                num_rooms_2 = random.randint(20, 100)  # randomly generate number of single rooms
                price_1 = int(price_2 * random.uniform(0.5, 1))  # populate single room prices randomly from double room prices
                num_rooms_1 = random.randint(10, 30)  # randomly generate number of double rooms
                for i in range(num_rooms_1):
                    cursor.execute("INSERT INTO room(room_no, num_people, price, hotel_id) VALUES(%s, %s, %s, %s)",
                                   [i+1, 1, price_1, hotel_id])
                for i in range(num_rooms_2):
                    cursor.execute("INSERT INTO room(room_no, num_people, price, hotel_id) VALUES(%s, %s, %s, %s)",
                                   [num_rooms_1+i+1, 2, price_2, hotel_id])
            connection.commit()

        print("Executed successfully ")

    except mysql.connector.Error as error:
        print("Failed to execute: {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

        con.close()
        engine.dispose()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--host', type=str, default='localhost')
    parser.add_argument('--database', type=str, default='hbms')
    parser.add_argument('--user', type=str, required=True)
    parser.add_argument('--password', type=str, required=True)

    args = parser.parse_args()

    main(args.user, args.password, args.host, args.database)