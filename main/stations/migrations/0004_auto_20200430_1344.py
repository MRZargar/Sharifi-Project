# Generated by Django 3.0.3 on 2020-04-30 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stations', '0003_auto_20200430_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setup',
            name='operator_name',
            field=models.CharField(max_length=255),
        ),
    ]