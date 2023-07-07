import math

from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from NewsFeed.forms import CreateNewsForm
from NewsFeed.models import NewsArticle, Comment
from UserSystem.models import CustomUser


class IndexView(generic.ListView):
    template_name = 'NewsFeed/index.html'
    context_object_name = 'latest_article_list'

    def get_queryset(self):
        """Return the last ten published articles."""
        return NewsArticle.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


# Create your views here.


class DetailView(generic.DetailView):
    model = NewsArticle
    template_name = 'NewsFeed/detail.html'

    def get_queryset(self):
        """
        Excludes any articles that aren't published yet.
        """
        return NewsArticle.objects.filter(pub_date__lte=timezone.now())

#Checking permissions in a template: {{ perms.catalog.can_mark_returned }}
#Checking permissions in views using decorator:
#@permission_required('catalog.can_edit')

#you can also check permissions using mixin in views
#class MyView(PermissionRequiredMixin, View):
#   permission_required = 'catalog.can_mark_returned'
#    # Or multiple permissions
#    permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')
#    # Note that 'catalog.can_edit' is just an example
#    # the catalog application doesn't have such permission!


@login_required
def send_comment(request, article_id):
    if request.user.is_authenticated:
        article = get_object_or_404(NewsArticle, pk=article_id)
        q = Comment(article=article, user_id=request.user, pub_datetime=timezone.now(), comment_text=request.POST['comment_text'])
        q.save()
    return HttpResponseRedirect(reverse('NewsFeed:detail', args=(article_id,)))


def index_using_culling(request, page_num='1'):
    all_articles = NewsArticle.objects.filter(pub_date__lte=timezone.now())
    articles_count = all_articles.count()
    latest_article_list = all_articles[(int(page_num) - 1) * 5:int(page_num) * 5]

    for item in latest_article_list:
        item.news_text = item.news_text[:item.news_main_text_culling]
    context = {'latest_article_list': latest_article_list}

    total_pages = int(math.ceil(articles_count / 5))

    slice_radius = 4
    if int(page_num) > slice_radius:
        first_slice = int(page_num)-slice_radius-1
    else:
        first_slice = 1
    second_slice = int(page_num)+slice_radius

    page_numbers = [x for x in range(1, total_pages + 1)][first_slice:second_slice]

    #adding first and last page if they are not present already
    if len(page_numbers):
        if page_numbers[0] != 1:
            page_numbers.insert(0, 1)
        if page_numbers[-1] != total_pages:
            page_numbers.append(total_pages)

    context['page_numbers'] = page_numbers
    context['current_page'] = page_num

    return render(request, 'NewsFeed/index.html', context)

# add the reference to the last page
    # Код надо наверное отрефакторить?

def tag_filtered(request, tag_name, page_num='1'):
    all_articles = NewsArticle.objects.filter(tags__tag_name=tag_name).filter(pub_date__lte=timezone.now())
    articles_count = all_articles.count()
    latest_article_list = all_articles[(int(page_num) - 1) * 5:int(page_num) * 5]
    for item in latest_article_list:
        item.news_text = item.news_text[:item.news_main_text_culling]
    context = {'latest_article_list': latest_article_list}

    total_pages = int(math.ceil(articles_count / 5))
    page_numbers = [x for x in range(1, total_pages + 1)][:7]
    if total_pages > 8:
        page_numbers.append(total_pages)  # add the reference to the last page
    context['page_numbers'] = page_numbers #Код надо наверное отрефакторить?
    context['tag'] = tag_name
    return render(request, 'NewsFeed/index.html', context)

#TODO: Medium priority: make tag reset button (Should be easy really, use ?=next) DONE

@permission_required('core.can_create_news')
def create_article_view(request):
    if request.method == 'POST':
        form = CreateNewsForm(request.POST)
        if form.is_valid():
            article = NewsArticle(news_title=form.cleaned_data['news_title'], news_text=form.cleaned_data['news_text'], author=request.user)
            article.save()
            article.tags.set(form.cleaned_data['tags'])
            return HttpResponseRedirect(reverse('NewsFeed:detail', args=[int(article.id)]))
    else:
        form = CreateNewsForm()
        return render(request, 'NewsFeed/article_form.html', {'form': form})