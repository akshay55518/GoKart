# Generated by Django 5.0.1 on 2024-01-30 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gokart', '0007_alter_brand_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=20)),
                ('lname', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('gender', models.CharField(max_length=5)),
                ('city', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
    ]