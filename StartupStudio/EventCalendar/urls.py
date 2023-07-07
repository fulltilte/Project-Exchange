from django.urls import path, include

from . import views

app_name = 'EventCalendar'
urlpatterns = [
    path('', views.IndexUsingCulling, name='events'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('event_tag=<str:tag_name>/', views.tag_filtered, name='events_tag_filtered'),
    path('event/<int:event_id>/sendcomment', views.send_comment, name='send_comment'),
]



#you can also do like that: event/<int:event_id>/<int:some_param>/ to intercept multiple parameters
#in here: event_id and some_param are the names of the variables and as such they should be
#initiated in params of view with the very same names
