# Generated by Django 4.2.4 on 2023-09-29 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_damagedproducts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='damagedproducts',
            name='qty',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
