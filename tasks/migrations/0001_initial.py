# Generated by Django 4.1.5 on 2023-06-13 03:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name="Task",
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
                ("title", models.CharField(max_length=255)),
                ("description", models.CharField(max_length=255)),
                ("due_date", models.DateTimeField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("P", "Pending"),
                            ("C", "Completed"),
                            ("IP", "In Progress"),
                        ],
                        default="P",
                        max_length=2,
                    ),
                ),
                (
                    "priority",
                    models.CharField(
                        choices=[("H", "High"), ("M", "Medium"), ("L", "Low")],
                        max_length=2,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("last_updated_on", models.DateTimeField(auto_now=True)),
                ("categories", models.ManyToManyField(to="tasks.category")),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Tasks",
                "ordering": [
                    "due_date",
                    "priority",
                    "status",
                    "-last_updated_on",
                    "-created_on",
                ],
            },
        ),
    ]
