# Generated by Django 3.0.3 on 2020-05-13 07:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='content',
            new_name='send_content',
        ),
    ]
