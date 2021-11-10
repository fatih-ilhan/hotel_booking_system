import mysql.connector
from sqlalchemy import create_engine

from format_data import format_hotels_data


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
    delete_table_command = """ DROP TABLE room; """

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

    cursor.execute(delete_table_command)
    cursor.execute(create_room_table_command)

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
