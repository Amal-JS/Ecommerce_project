# Generated by Django 4.2.4 on 2023-10-02 11:05

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
            name='Coupons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('discount_percentage', models.IntegerField()),
                ('cart_min_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('valid_to', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('coupoun_type', models.CharField(choices=[('general', 'General Coupoun'), ('category', 'Category Coupoun'), ('variant', 'Product Coupoun')], max_length=20)),
                ('coupoun_applied_to', models.CharField(blank=True, max_length=400, null=True)),
                ('count', models.PositiveIntegerField()),
                ('cart_max_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount_amount', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='UsedCoupons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupons', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_coupons', to='coupoun.coupons')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Used Coupons',
            },
        ),
    ]