# Generated by Django 3.0.3 on 2020-05-28 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0005_message_messagetype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='messageType',
            field=models.CharField(default='send', max_length=10),
        ),
    ]
