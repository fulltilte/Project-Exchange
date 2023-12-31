# Generated by Django 4.0.1 on 2022-03-05 16:30

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='NewsArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news_title', models.CharField(max_length=200)),
                ('pub_date', models.DateField(verbose_name='date published')),
                ('news_text', models.TextField(max_length=80000)),
                ('news_main_text_culling', models.IntegerField(default=800, validators=[django.core.validators.MaxValueValidator(800), django.core.validators.MinValueValidator(1)])),
                ('tags', models.ManyToManyField(to='NewsFeed.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.CharField(max_length=600)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NewsFeed.newsarticle')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
