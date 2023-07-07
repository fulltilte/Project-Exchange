from django.urls import path, include
from . import views

app_name = 'NewsFeed'
urlpatterns = [
    path('', views.index_using_culling, name='news'),
    path('<int:page_num>/', views.index_using_culling, name='news_on_page'), #open desired page
    path('article/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('tag=<str:tag_name>/', views.tag_filtered, name='news_tag_filtered'),
    path('tag=<str:tag_name>/<int:page_num>/', views.tag_filtered, name='news_tag_filtered_with_page_num'),
    path('article/<int:article_id>/sendcomment', views.send_comment, name='send_comment'),
    path('article/create', views.create_article_view, name='create_article'),
]

urlpatterns += [
    path('markdownx/', include('markdownx.urls')),
]
#put create news here btw
    #Maybe i should make tags as parameters for get view