# Generated by Django 5.0.1 on 2024-01-30 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gokart', '0006_alter_category_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='id',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
    ]