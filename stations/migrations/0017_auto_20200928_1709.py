# Generated by Django 3.0.3 on 2020-09-28 13:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stations', '0016_auto_20200928_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setup',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 28, 17, 9, 17, 196207)),
        ),
        migrations.AlterField(
            model_name='setup',
            name='health_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 28, 17, 9, 17, 196520)),
        ),
    ]
