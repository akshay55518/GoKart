# Generated by Django 5.0.1 on 2024-02-05 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Gokart', '0023_orderplaced_delete_payment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OrderPlaced',
        ),
    ]
