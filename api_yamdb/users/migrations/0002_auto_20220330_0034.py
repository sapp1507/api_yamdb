# Generated by Django 2.2.16 on 2022-03-30 00:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={"ordering": ["id"]},
        ),
    ]