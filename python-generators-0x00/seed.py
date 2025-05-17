import csv
import uuid
import mysql.connector 
from mysql.connector import errorcode
from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = os.getenv('DB_NAME', 'alx_prodev')

def connect_db():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )

def create_database(connection):
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Database '{DB_NAME}' created successfully")
    finally:
        cursor.close()

def connect_to_prodev():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=DB_NAME,
    )

def create_table(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(5, 2) NOT NULL,
                INDEX (user_id)
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
                print(f"Inserted {name} into user_data")
        connection.commit()
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

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("❌ Invalid username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("❌ Database does not exist")
        else:
            print("❌", err)
