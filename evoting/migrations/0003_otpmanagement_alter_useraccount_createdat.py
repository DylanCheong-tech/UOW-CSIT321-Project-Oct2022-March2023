# Generated by Django 4.1.4 on 2022-12-30 13:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evoting', '0002_alter_useraccount_createdat'),
    ]

    operations = [
        migrations.CreateModel(
            name='OTPManagement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='createdAt',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 30, 13, 59, 38, 754663, tzinfo=datetime.timezone.utc)),
        ),
    ]
