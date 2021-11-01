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

    create_hotel_table_command = """ CREATE TABLE HOTEL
                                    (
                                      id              INT unsigned NOT NULL AUTO_INCREMENT,
                                      name            VARCHAR(150) NOT NULL,
                                      address         VARCHAR(150) NOT NULL,
                                      zip_code        VARCHAR(10) NOT NULL,
                                      phone           VARCHAR(15) NOT NULL,
                                      web_url         VARCHAR(500),
                                      PRIMARY KEY     (id)
                                    ); 
                                 """
    delete_hotel_table_command = """ DROP TABLE HOTEL; """

    show_table_command = """ SELECT * FROM HOTEL; """

    # cursor.execute(delete_hotel_table_command)
    cursor.execute(create_hotel_table_command)

    df = format_hotels_data()
    df = df[df.name.isnull() == False]
    df.to_sql(con=con, name='HOTEL', if_exists='append', index=False, index_label='id')

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
