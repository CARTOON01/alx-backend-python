import csv
import uuid
import mysql.connector 
from mysql.connector import errorcode

DB_NAME = 'alx_prodev'

def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='alx_prodev',
        password='alx_prodev',
    )

def create_database(connection):
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Database {DB_NAME} created successfully")

    finally:
        cursor.close()

def connect_to_prodev():
    return mysql.connector.connect(
        host='localhost',
        user='alx_prodev',
        password='alx_prodev',
        database=DB_NAME,
    )

def create_table(connection):
    cursor = connection.cursor()
    try:
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age Decimal(5, 2) NOT NULL,
                INDEX (user_id),
            )
        """)
        print('Table "user_data" created successfully')
    finally:
        cursor.close()

def insert_data(connection, data):
    cursor = connection.cursor()
    try: 
        for row in data:
            name, email, age = row
            user_id = str(uuid.uuid4())

            cursor.execute("SELECT COUNT(*) FROM user_data WHERE email = %s", (email,))
            if cursor.fetchone()[0] == 0:
                cursor.execute(
                    "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                    (user_id, name, email, age)
                )
            connection.commit()
            print(f"Inserted {name} into user_data")
    finally:
        cursor.close()
        connection.close()

def read_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        return list(reader)
if __name__ == "__main__":
    try:
        conn = connect_db()
        create_database(conn)
        conn.close()

        conn = connect_to_prodev()
        create_table(conn)
        user_data = read_csv('user_data.csv')
        insert_data(conn, user_data)
        conn.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)