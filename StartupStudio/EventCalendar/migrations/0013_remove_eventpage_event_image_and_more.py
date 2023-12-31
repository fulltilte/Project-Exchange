# Generated by Django 4.0.1 on 2022-06-05 09:50

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('EventCalendar', '0012_alter_eventpage_ending_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventpage',
            name='event_image',
        ),
        migrations.RemoveField(
            model_name='eventpage',
            name='event_prize',
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='event_text',
            field=markdownx.models.MarkdownxField(),
        ),
    ]
