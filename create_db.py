import random

import mysql.connector
from django.db import connection
from sqlalchemy import create_engine

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='hbms',
                                         user='fi',
                                         password='fthgS1905-')

    engine = create_engine("mysql://fi:fthgS1905-@localhost/hbms")
    con = engine.connect()

    cursor = connection.cursor()

    create_hotel_table_command = """ CREATE TABLE hotel
                                    (
                                      id              INT unsigned NOT NULL AUTO_INCREMENT,
                                      name            VARCHAR(150) NOT NULL,
                                      address         VARCHAR(150) NOT NULL,
                                      zip_code        VARCHAR(10) NOT NULL,
                                      phone           VARCHAR(15) NOT NULL,
                                      web_url         VARCHAR(500),
                                      manager_id      BIGINT DEFAULT 2,
                                      FOREIGN KEY     (manager_id) REFERENCES users_user(id),
                                      PRIMARY KEY     (id)
                                    ); 
                                 """
    delete_room_table_command = """ DROP TABLE room; """
    delete_reservation_table_command = """ DROP TABLE reservation; """
    delete_reserved_room_table_command = """ DROP TABLE reserved_room; """

    show_table_command = """ SELECT * FROM room; """

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
                                              FOREIGN KEY     (res_id) REFERENCES reservation(id),
                                              FOREIGN KEY     (room_id) REFERENCES room(id),
                                              PRIMARY KEY     (id)
                                            ); 
                                         """

    cursor.execute(delete_reserved_room_table_command)
    cursor.execute(delete_reservation_table_command)
    cursor.execute(delete_room_table_command)
    cursor.execute(create_room_table_command)
    cursor.execute(create_reservation_table_command)
    cursor.execute(create_reserved_room_table_command)

    fill_rooms = True
    if fill_rooms:
        for hotel_id in range(1, 169):
            price_1 = random.randint(75, 300)
            num_rooms_1 = random.randint(10, 30)
            price_2 = int(price_1 * random.uniform(1.5, 2))
            num_rooms_2 = random.randint(20, 100)
            for i in range(num_rooms_1):
                cursor.execute("INSERT INTO room(room_no, num_people, price, hotel_id) VALUES(%s, %s, %s, %s)",
                               [i+1, 1, price_1, hotel_id])
            for i in range(num_rooms_2):
                cursor.execute("INSERT INTO room(room_no, num_people, price, hotel_id) VALUES(%s, %s, %s, %s)",
                               [num_rooms_1+i+1, 2, price_2, hotel_id])
        connection.commit()

    # df = format_hotels_data()
    # df = df[df.name.isnull() == False]
    # df.to_sql(con=con, name='hotel', if_exists='append', index=False, index_label='id')

    result = engine.execute(show_table_command).fetchall()

    print("Executed successfully ")
    print(result)

except mysql.connector.Error as error:
    print("Failed to execute for table in MySQL: {}".format(error))
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")

    con.close()
    engine.dispose()
