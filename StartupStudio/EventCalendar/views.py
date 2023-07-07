from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from EventCalendar.models import EventPage, EventComment
from UserSystem.models import CustomUser


def IndexUsingCulling(request):
    latest_event_list = EventPage.objects.filter(pub_date__lte=timezone.now())[:10]
    for item in latest_event_list:
        item.event_text = item.event_text[:item.event_main_text_culling]
    context = {'latest_event_list': latest_event_list}
    return render(request, 'EventCalendar/index.html', context)
    #paginate_by = 10 - pagination
    #events/?page=2 go to page 2 using GET paramethers
    #TODO: Events paginations through ListView pagination


class DetailView(generic.DetailView):
    model = EventPage
    template_name = 'EventCalendar/detail.html'

    def get_queryset(self):
        """
        Excludes any articles that aren't published yet.
        """
        return EventPage.objects.filter(pub_date__lte=timezone.now())


@login_required
def tag_filtered(request, tag_name):
    latest_event_list = EventPage.objects.filter(event_tags__tag_name=tag_name).filter(pub_date__lte=timezone.now())[:10]
    for item in latest_event_list:
        item.event_text = item.event_text[:item.event_main_text_culling]
    context = {'latest_event_list': latest_event_list}
    context['tag'] = tag_name
    return render(request, 'EventCalendar/index.html', context)
# Create your views here.


#TODO: MEDIUM PRIO: Проверить, все ли view написаны корректно, и можно ли заменить некоторые на обобщенные
def send_comment(request, event_id):
    if request.user.is_authenticated:
        event = get_object_or_404(EventPage, pk=event_id)
        q = EventComment(article=event, user_id=request.user, pub_datetime=timezone.now(), comment_text=request.POST['comment_text'])
        q.save()
    return HttpResponseRedirect(reverse('EventCalendar:detail', args=(event_id,)))


