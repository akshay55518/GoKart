# Generated by Django 5.0 on 2024-03-24 19:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gokart', '0034_delete_orderplaced'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderPlaced',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveBigIntegerField(default=1)),
                ('ordered_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Accepted', 'Accepted'), ('Packed', 'Packed'), ('Rejected', 'Rejected'), ('Pending', 'Pending'), ('On the Way', 'On the Way'), ('Delivered', 'Delivered')], default='Pending', max_length=50)),
                ('payment', models.CharField(choices=[('COD', 'Cash on Delivery'), ('RazorPay', 'RazorPay')], default='COD', max_length=100)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Gokart.customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Gokart.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
