# Generated by Django 4.2.4 on 2023-09-26 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='star_rating',
            field=models.PositiveIntegerField(default=0),
        ),
    ]