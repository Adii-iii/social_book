# Generated by Django 4.1.7 on 2023-03-20 10:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0002_customuser_first_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("author", models.CharField(max_length=200)),
                ("file_type", models.CharField(max_length=10)),
                ("file_path", models.CharField(max_length=200)),
            ],
        ),
    ]
