# Generated by Django 4.1 on 2022-12-07 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("db", "0004_alter_classroom_classroom_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user", name="user_type", field=models.IntegerField(),
        ),
    ]