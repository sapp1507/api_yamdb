import csv
import sqlite3
from datetime import date
from pathlib import Path

path_to_db = Path('api_yamdb', 'db.sqlite3')
path_to_file = Path('api_yamdb', 'static', 'data', 'users.csv')
today_date = str(date.today())


def get_querry(user_data):
    return """INSERT INTO users_user (username, email, role,
                                bio, first_name, last_name,
                                password, is_superuser, is_staff,
                                is_active, date_joined)
                        VALUES ('{1}','{2}','{3}',
                                '{4}','{5}','{6}',
                                '', '0', '0',
                                '1', {7});""".format(*user_data, today_date)


def main(path_to_file):
    conn = sqlite3.connect(path_to_db)
    cursor = conn.cursor()
    with open(path_to_file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            querry = get_querry(row)
            cursor.execute(querry)
    conn.commit()


if __name__ == '__main__':
    main(path_to_file)
