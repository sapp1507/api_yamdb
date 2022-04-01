import csv
import sqlite3
from datetime import date
from pathlib import Path

"""Для импорта данных используются след. механизмы: 
1) Дата миграции https://docs.djangoproject.com/en/3.1/topics/migrations/#data-migrations 
2) Кастомная команда https://docs.djangoproject.com/en/3.1/howto/custom-management-commands/ 
3) Загрузка фикстур https://docs.djangoproject.com/en/3.1/howto/initial-data/#:~:text=You'll%20store%20this%20data,re%2Dloaded%20into%20the%20database.
Не стоит привязываться к конкретной БД - используйте ORM. Это универсальный механизм для работы с разными типами БД."""

path_to_db = Path('api_yamdb', 'db.sqlite3')
path_to_file = Path('api_yamdb', 'static', 'data', 'users.csv')
today_date = date.today()


def get_querry(user_data):
<<<<<<< HEAD
    querry = (
        "INSERT INTO users_user (id, username, email, role,"
        " bio, first_name, last_name, password, is_superuser, is_staff,"
        "is_active, date_joined)"
        "VALUES ({0},'{1}','{2}','{3}','{4}','{5}','{6}',"
        "'', '0', '0','1', '{7}');").format(*user_data, today_date)
    return querry
=======
    return """INSERT INTO users_user (username, email, role,
                                bio, first_name, last_name,
                                password, is_superuser, is_staff,
                                is_active, date_joined)
                        VALUES ('{1}','{2}','{3}',
                                '{4}','{5}','{6}',
                                '', '0', '0',
                                '1', {7});""".format(*user_data, today_date)
>>>>>>> 282a5299623b1543c9b45d7de5ad736ea8161d45


def main(path_to_file):
    conn = sqlite3.connect(path_to_db)
    cursor = conn.cursor()
    with open(path_to_file, 'r') as csvfile:
        csvfile.readline()
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            querry = get_querry(row)
            cursor.execute(querry)
    conn.commit()


if __name__ == '__main__':
    main(path_to_file)
