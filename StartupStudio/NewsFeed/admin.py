from django.contrib import admin

from .models import NewsArticle
from .models import Tag
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'user_id', 'comment_text', 'pub_datetime')
    pass

admin.site.register(NewsArticle)
admin.site.register(Tag)
#admin.site.register(Comment)

# Register your models here.
