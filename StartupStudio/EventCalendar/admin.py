from django.contrib import admin

from .models import EventPage, EventComment
from .models import EventTag


@admin.register(EventComment)
class EventCommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'user_id', 'comment_text', 'pub_datetime')
    pass


@admin.register(EventPage)
class EventPageAdmin(admin.ModelAdmin):
    list_display = ('event_title', 'pub_date', 'start_date', 'ending_date', 'entry_deadline')


admin.site.register(EventTag)
