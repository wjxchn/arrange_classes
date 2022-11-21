# Generated by Django 4.1 on 2022-11-21 09:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Author",
            fields=[
                ("nid", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=32)),
                ("age", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Publish",
            fields=[
                ("nid", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=32)),
                ("city", models.CharField(max_length=32)),
                ("email", models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name="Book",
            fields=[
                ("nid", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=32)),
                ("publishDate", models.DateField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=5)),
                ("author", models.ManyToManyField(to="db.author")),
                (
                    "publish",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="db.publish"
                    ),
                ),
            ],
        ),
    ]