# Generated by Django 5.0.1 on 2024-02-02 04:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Gokart', '0014_cart_cartitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='product',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='user',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
    ]