# Generated by Django 4.1.4 on 2023-01-02 07:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evoting', '0008_alter_otpmanagement_expireat_alter_useraccount_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpmanagement',
            name='expireAt',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 2, 7, 11, 12, 266710, tzinfo=datetime.timezone.utc)),
        ),
    ]