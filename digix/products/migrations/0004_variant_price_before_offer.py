# Generated by Django 4.2.4 on 2023-10-04 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_variant_tv_mount'),
    ]

    operations = [
        migrations.AddField(
            model_name='variant',
            name='price_before_offer',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
    ]