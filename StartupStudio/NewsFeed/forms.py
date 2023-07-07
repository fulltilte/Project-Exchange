from django.forms import ModelForm

from NewsFeed.models import NewsArticle


class CreateNewsForm(ModelForm):
    class Meta:
        model = NewsArticle
        fields = ['news_title', 'news_text', 'tags']
        labels = {'news_title':'Заголовок', 'news_text':'Текст статьи', 'tags':'Тэги'}
