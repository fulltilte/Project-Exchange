import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

from UserSystem.models import CustomUser


class EventTag(models.Model):
    tag_name = models.CharField(max_length=40)

    def __str__(self):
        return self.tag_name


class EventPage(models.Model):
    event_title = models.CharField(max_length=200)
    pub_date = models.DateField('date published')
    start_date = models.DateTimeField('start date')
    ending_date = models.DateTimeField('ending date')
    entry_deadline = models.DateTimeField('entry deadline')
    event_organiser = models.CharField(max_length=60)
    event_text = MarkdownxField()
    event_image = models.CharField('link to the picture used in the post', max_length=400, null=True, blank=True)
    event_tags = models.ManyToManyField(EventTag) #Tag Fields following Many to Many rules
    event_main_text_culling = models.IntegerField(  # providing minimal and max values for text Culling
        default=800,
        validators=[
            MaxValueValidator(800),
            MinValueValidator(1)
        ]
    )
    author = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return self.event_title

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=4) <= self.pub_date <= now

    def formatted_markdown(self):
        return markdownify(self.event_text)


class EventComment(models.Model):
    article = models.ForeignKey(EventPage, on_delete=models.CASCADE)
#    user_name = models.CharField(max_length=30)
    user_id = models.ForeignKey(CustomUser,  null=True, on_delete=models.SET_NULL)
    comment_text = models.CharField(max_length=600)
    pub_datetime = models.DateTimeField('date published')

    class Meta:
        ordering = ["pub_datetime"]

    def __str__(self):
        return self.user_id.username + ": " + str(self.comment_text)[:20] + " at " + str(self.pub_datetime.strftime("%Y-%m-%d %H:%M:%S"))


# Create your models here.
