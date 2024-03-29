# Generated by Django 2.2.3 on 2020-12-11 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mustbuy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=30)),
                ('trackid', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'axf_mustbuy',
            },
        ),
        migrations.CreateModel(
            name='Nav',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=30)),
                ('trackid', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'axf_nav',
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=30)),
                ('trackid', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'axf_shop',
            },
        ),
    ]
