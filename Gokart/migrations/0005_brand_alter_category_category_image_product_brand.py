# Generated by Django 5.0.1 on 2024-01-30 02:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gokart', '0004_banner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=50)),
                ('brand_logo', models.ImageField(upload_to='product/brand')),
            ],
        ),
        migrations.AlterField(
            model_name='category',
            name='category_image',
            field=models.ImageField(upload_to='product/Category'),
        ),
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Gokart.brand'),
        ),
    ]
