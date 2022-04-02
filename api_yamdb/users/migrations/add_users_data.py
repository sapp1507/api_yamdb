import csv
import os
from pathlib import Path

from django.db import migrations

base_dir = os.path.dirname(os.path.realpath(__file__))
path_to_file = Path(Path(base_dir).parent.parent,
                    'static', 'data', 'users.csv')


def get_data(row):

    data = {
        'id': row[0],
        'username': row[1],
        'email': row[2],
        'role': row[3],
        'bio': row[4],
        'first_name': row[5],
        'last_name': row[6],
    }
    return data


def add_users(apps, schema_editor):
    User = apps.get_model('users', 'User')
    with open(path_to_file, 'r') as csvfile:
        csvfile.readline()
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            data = get_data(row)
            user = User.objects.create(**data)
            user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20220401_2215'),
    ]

    operations = [
        migrations.RunPython(add_users),
    ]
