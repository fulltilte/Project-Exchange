# Generated by Django 4.0.1 on 2022-05-15 13:11

import datetime
from django.db import migrations, models
import django.utils.timezone
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_projectentry_status_alter_teamentry_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='project_end',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Project Ending'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='project_start',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Project Start'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2022, 5, 15, 13, 10, 11, 998668, tzinfo=utc), verbose_name='Date Time published'),
        ),
    ]
