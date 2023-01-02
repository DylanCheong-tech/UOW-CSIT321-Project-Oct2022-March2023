# Generated by Django 4.1.4 on 2022-12-30 13:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('accountID', models.BigAutoField(default=1, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=22)),
                ('firstName', models.CharField(max_length=50)),
                ('lastName', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=1)),
                ('createdAt', models.DateTimeField(default=datetime.datetime(2022, 12, 30, 13, 35, 21, 684377, tzinfo=datetime.timezone.utc))),
            ],
        ),
    ]
