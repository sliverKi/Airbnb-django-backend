# Generated by Django 4.1.5 on 2023-02-06 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rooms", "0006_alter_room_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="room",
            name="price",
            field=models.PositiveBigIntegerField(),
        ),
    ]
