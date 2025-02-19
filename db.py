import sqlite3
from functools import wraps, lru_cache

from constants import TOKENS_NAMES, TOKENS


def open_close_db_decorator(func):
    """Подключение и отключение к базе данных."""
    @wraps(func)
    def wrapper(*args, **kwrgs):
        con = sqlite3.connect('my_database.db')
        cursor = con.cursor()
        result = func(cursor=cursor, *args, **kwrgs)
        con.commit()
        con.close()
        return result
    return wrapper


@open_close_db_decorator
def make_db(cursor):
    """Создаём базу данных."""
    cursor.executescript('''
    CREATE TABLE IF NOT EXISTS bags(
        id INTEGER PRIMARY KEY,
        plus_one_tokens INTEGER DEFAULT 0,
        zero_tokens INTEGER DEFAULT 0,
        minus_one_tokens INTEGER DEFAULT 0,
        minus_two_tokens INTEGER DEFAULT 0,
        minus_tree_tokens INTEGER DEFAULT 0,
        minus_four_tokens INTEGER DEFAULT 0,
        minus_five_tokens INTEGER DEFAULT 0,
        minus_six_tokens INTEGER DEFAULT 0,
        minus_seven_tokens INTEGER DEFAULT 0,
        minus_eight_tokens INTEGER DEFAULT 0,
        star_tokens INTEGER DEFAULT 0,
        tentacle_tokens INTEGER DEFAULT 0,
        kthulhu_tokens INTEGER DEFAULT 0,
        hood_tokens INTEGER DEFAULT 0,
        skull_tokens INTEGER DEFAULT 0,
        tablet_tokens INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS users_stats(
        id INTEGER PRIMARY KEY,
        plus_one_tokens INTEGER DEFAULT 0,
        zero_tokens INTEGER DEFAULT 0,
        minus_one_tokens INTEGER DEFAULT 0,
        minus_two_tokens INTEGER DEFAULT 0,
        minus_tree_tokens INTEGER DEFAULT 0,
        minus_four_tokens INTEGER DEFAULT 0,
        minus_five_tokens INTEGER DEFAULT 0,
        minus_six_tokens INTEGER DEFAULT 0,
        minus_seven_tokens INTEGER DEFAULT 0,
        minus_eight_tokens INTEGER DEFAULT 0,
        star_tokens INTEGER DEFAULT 0,
        tentacle_tokens INTEGER DEFAULT 0,
        kthulhu_tokens INTEGER DEFAULT 0,
        hood_tokens INTEGER DEFAULT 0,
        skull_tokens INTEGER DEFAULT 0,
        tablet_tokens INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY UNIQUE,
        bag_id INTEGER NOT NULL UNIQUE,
        user_stats_id INTEGER NOT NULL UNIQUE,
        FOREIGN KEY(bag_id) REFERENCES bags(id),
        FOREIGN KEY(user_stats_id) REFERENCES users_stats(id)
    );
    ''')


@open_close_db_decorator
def new_user(cursor, id):
    """Создаёт запись в БД для нового пользователя."""
    cursor.execute(
        '''
        SELECT id
        FROM users
        WHERE id = (?)
        ''',
        (id,)
    )
    data_in_db = cursor.fetchall()
    if not data_in_db:
        cursor.execute(
            '''
            INSERT INTO bags (id)
            VALUES (?)
            ''',
            (id,)
        )
        cursor.execute(
            '''
            INSERT INTO users_stats (id)
            VALUES (?)
            ''',
            (id,)
        )
        cursor.execute(
            '''INSERT INTO users
            VALUES (?, ?, ?)
            ''',
            (id, id, id)
        )


@open_close_db_decorator
def add_token(cursor, token, table, id):
    """Добавляет токен в мешок или в статистику пользователя."""
    column = TOKENS_NAMES.get(token)
    request = f'UPDATE {table} SET {column} = {column} + 1 WHERE id = {id}'
    cursor.execute(request)

@open_close_db_decorator
def get_bag_from_db(cursor, id):
    """Возвращает мешок в виде списка лежащих в нём жетонов."""
    columns = ', '.join(TOKENS_NAMES.values())
    request = f'SELECT {columns} FROM bags WHERE id = {id}'
    cursor.execute(request)
    tokens_vals_set = tuple(zip(TOKENS, cursor.fetchall()[0]))
    token_set = []
    for token_val in tokens_vals_set:
        token, val = token_val
        for _ in range(val):
            token_set.append(token)
    return token_set


@open_close_db_decorator
def delete_token(cursor, token, table, id):
    """Удаляет жетон из мешка."""
    column = TOKENS_NAMES.get(token)
    request = f'UPDATE {table} SET {column} = {column} - 1 WHERE id = {id}'
    cursor.execute(request)

def main():
    make_db()


if __name__ == '__main__':
    main()
