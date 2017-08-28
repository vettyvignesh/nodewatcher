# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-09 18:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('irnas_koruzav2', '0004_json_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='koruzamonitor',
            name='accel_x_range1',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='koruzamonitor',
            name='accel_x_range1_maximum',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='koruzamonitor',
            name='accel_x_range2',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='koruzamonitor',
            name='accel_x_range2_maximum',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='koruzamonitor',
            name='accel_x_range3',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='koruzamonitor',
            name='accel_x_range3_maximum',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='koruzamonitor',
            name='accel_x_range4',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='koruzamonitor',
            name='accel_x_range4_maximum',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='koruzamonitor',
            name='accel_y_range1',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='koruzamonitor',
            name='accel_y_range1_maximum',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='koruzamonitor',
            name='accel_y_range2',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='koruzamonitor',
            name='accel_y_range2_maximum',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='koruzamonitor',
            name='accel_y_range3',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='koruzamonitor',
            name='accel_y_range3_maximum',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='koruzamonitor',
            name='accel_y_range4',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='koruzamonitor',
            name='accel_y_range4_maximum',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='koruzamonitor',
            name='accel_z_range1',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='koruzamonitor',
            name='accel_z_range1_maximum',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='koruzamonitor',
            name='accel_z_range2',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='koruzamonitor',
            name='accel_z_range2_maximum',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='koruzamonitor',
            name='accel_z_range3',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='koruzamonitor',
            name='accel_z_range3_maximum',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='koruzamonitor',
            name='accel_z_range4',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='koruzamonitor',
            name='accel_z_range4_maximum',
            field=models.FloatField(null=True),
        ),
    ]
