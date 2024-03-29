# Generated by Django 5.0.1 on 2024-01-30 15:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gokart', '0008_userregistration'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=100)),
                ('locality', models.CharField(max_length=50)),
                ('landmark', models.CharField(max_length=100)),
                ('mobile', models.IntegerField()),
                ('pincode', models.IntegerField()),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Gokart.userregistration')),
            ],
        ),
    ]
