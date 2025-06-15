#!/usr/bin/python3
seed = __import__('seed')

def paginate_users(page_size, offset):
    connection = seed.connect_to_prodev()
    cusor = connection.cursor(dictionary=True)
    cusor.execute("SELECT * FROM user_data LIMIT  {page_size} OFFSET {offset}")
    rows = cusor.fetchall()
    connection.close()
    return rows

def lazy_pagination(page_size):
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size