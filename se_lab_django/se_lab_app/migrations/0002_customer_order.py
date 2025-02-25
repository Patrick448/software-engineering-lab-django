# Generated by Django 5.1.2 on 2024-11-06 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('se_lab_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('status', models.CharField(max_length=20)),
            ],
        ),
    ]
