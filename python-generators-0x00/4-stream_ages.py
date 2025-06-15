#!/usr/bin/python3
seed = __import__('seed')

def stream_user_ages():
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictonary=True)
    cursor.execute("SELECT age FROM user_data")
    while True:
        row = cursor.fetchone()
        if not row:
            break
        yield row['age']
    connection.close()

def compute_average_age():
    total_age = 0
    count = 0
    for age in stream_user_ages():
        total_age += age
        count += 1
    if count == 0:
        print("Average age: 0")
    else:
        average_age = total_age / count
        print(f"Average age of users: {average_age:.2f}")

if __name__ == "__main__":
    compute_average_age()