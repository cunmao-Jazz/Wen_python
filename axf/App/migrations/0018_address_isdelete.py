# Generated by Django 2.2.3 on 2020-12-30 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0017_order_isdelete'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='isDelete',
            field=models.BooleanField(default=False, verbose_name='是否删除'),
        ),
    ]
