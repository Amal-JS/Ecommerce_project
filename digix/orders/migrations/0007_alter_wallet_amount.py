# Generated by Django 4.2.4 on 2023-09-29 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_wallet_walletusage_returnorder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
