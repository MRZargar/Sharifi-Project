# Generated by Django 3.0.3 on 2020-09-28 15:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stations', '0024_auto_20200928_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setup',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 28, 19, 28, 22, 955337)),
        ),
        migrations.AlterField(
            model_name='setup',
            name='health_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 28, 19, 28, 22, 955548)),
        ),
    ]
