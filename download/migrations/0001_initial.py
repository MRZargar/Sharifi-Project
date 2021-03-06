# Generated by Django 3.0.3 on 2020-09-25 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DownloadLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stations_id', models.CharField(max_length=2500)),
                ('from_date', models.CharField(max_length=20)),
                ('to_date', models.CharField(max_length=20)),
                ('start_hour', models.PositiveIntegerField()),
                ('end_hour', models.PositiveIntegerField()),
                ('download_link', models.CharField(blank=True, max_length=5000)),
                ('size', models.PositiveIntegerField(blank=True, null=True)),
                ('status', models.BooleanField(default=False)),
                ('request_date', models.DateTimeField(auto_now_add=True)),
                ('number', models.CharField(max_length=500, unique=True)),
                ('dic_delete', models.BooleanField(default=False)),
            ],
        ),
    ]
