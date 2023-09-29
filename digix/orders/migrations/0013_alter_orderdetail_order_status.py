# Generated by Django 4.2.4 on 2023-09-29 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_alter_returnorder_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='order_status',
            field=models.CharField(choices=[('order_pending', 'Order_Pending'), ('order_confirmed', 'Order_Confirmed'), ('shipped', 'Shipped'), ('cancelled', 'Cancelled'), ('delivered', 'Delivered'), ('waiting_for_approval', 'Waiting_For_Approval'), ('returned', 'Returned')], default='order_pending', max_length=100),
        ),
    ]
