# Generated by Django 2.1.8 on 2020-01-29 17:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coresetup', '0017_auto_20200129_0755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='mobile_number',
            field=models.BigIntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='registered_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 29, 17, 15, 45, 212243)),
        ),
    ]
