# Generated by Django 2.2.4 on 2019-09-26 15:59

import django.contrib.postgres.fields.ranges
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timeslot', '0004_auto_20190926_1258'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeslot',
            name='duration',
            field=django.contrib.postgres.fields.ranges.DateTimeRangeField(default=None),
            preserve_default=False,
        ),
    ]
