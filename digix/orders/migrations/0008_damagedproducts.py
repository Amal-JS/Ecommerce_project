# Generated by Django 4.2.4 on 2023-09-29 07:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_variant_tv_mount'),
        ('orders', '0007_alter_wallet_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='DamagedProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveIntegerField(default=1)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='damaged_products', to='products.variant')),
            ],
        ),
    ]
