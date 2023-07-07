from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

from UserSystem.models import CustomUser


import datetime


class Tag(models.Model):
    tag_name = models.CharField(max_length=20)

    def __str__(self):
        return self.tag_name


class NewsArticle(models.Model):
    news_title = models.CharField(max_length=200) #Rename news_title to article_title for better clarity
    pub_date = models.DateField('date published', default=timezone.now())
    news_text = MarkdownxField() #Rename news_text to article_text for better clarity
    tags = models.ManyToManyField(Tag) #Tag Fields following Many to Many rules
    news_main_text_culling = models.IntegerField(  # providing minimal and max values for text Culling
        default=800,
        validators=[
            MaxValueValidator(800),
            MinValueValidator(1)
        ]
    )
    author = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)


    def get_absolute_url(self):
        return reverse('NewsFeed:detail', args=[int(self.id)])

    def formatted_markdown(self):
        return markdownify(self.news_text)

    def __str__(self):
        return self.news_title

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=4) <= self.pub_date <= now

    class Meta:
        permissions = [
            ("create_new_news", "Can create new news"),
            ("delete_their_news", "Can delete their own news"),
            ("delete_any_news", "Can delete any news"),
        ]
        ordering = ["-pub_date"]


class Comment(models.Model):
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE)
#    user_name = models.CharField(max_length=30)
    user_id = models.ForeignKey(CustomUser,  null=True, on_delete=models.SET_NULL)
    comment_text = models.CharField(max_length=600)
    pub_datetime = models.DateTimeField('date published')

    class Meta:
        ordering = ["pub_datetime"]

    def __str__(self):
        return self.user_id.username + ": " +str(self.comment_text)[:20] + " at " + str(self.pub_datetime.strftime("%Y-%m-%d %H:%M:%S"))

    def get_absolute_url(self):
        return reverse('NewsFeed:detail', args=[int(self.article.id)])



#class NewsPreview(models.Model): #Probably is unneeded, but if someone likes the idea I can work on that
#    news_title = models.CharField(max_length=200)
#    news_text_preview = models.CharField(max_length=800) #Possible data duplication... is there any way to avoid it? #Maybe we should just mark the end of the preview in original text by invisible markdown
#    main_article_link = models.CharField(max_length=300) #Questionable decision, about to be hardcoded, weak to directory renames and such
#                                                         #Possible solution? swap it with a link to a model and make Django do the job of putting links in
#    pub_date = models.DateField('date published')  # Implementing preview culling is possible to prevent data duplication, while custom headers are still ?optional?
#
#    def __str__(self):
#        return self.news_title
#
#    def was_published_recently(self):
#        now = timezone.now()
#        return now - datetime.timedelta(days=4) <= self.pub_date <= now


# Create your models here.
