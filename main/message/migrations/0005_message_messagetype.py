# Generated by Django 3.0.3 on 2020-05-14 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0004_remove_message_is_replay'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='messageType',
            field=models.CharField(blank='send', max_length=10),
        ),
    ]
