# Generated by Django 5.0.6 on 2024-06-27 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_reservation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reservation",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "pending"),
                    ("accepted", "accepted"),
                    ("confirmed", "confirmed"),
                ],
                default="pending",
                max_length=50,
            ),
        ),
    ]
