from django.urls import path, reverse_lazy
from django.views.generic import RedirectView
from django.views.i18n import JavaScriptCatalog

from . import views

app_name = 'core'
urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register_request, name='register'),
    path('login', RedirectView.as_view(url=reverse_lazy('accounts/login/')), name='login_core'),
    path('logout', views.logout_view, name='logout'),
    path('projects/<int:pk>/', views.project_detail_view, name='project_detail'),
]

#team urls
urlpatterns += [
    path('projects/<int:pk>/teams', views.look_project_teams, name='project_teams'),
    path('projects/team/<int:team_pk>', views.team_detailed_view, name='team_detailed'),
    # basically a template for a team's page
    path('projects/<int:project_pk>/teams/create', views.create_team_view, name='project_teams_create'),
    # TODO: WIP And bottom too
    path('projects/teams/join', views.join_team_view, name='join_team'),
    path('projects/team/<int:team_pk>/applications', views.look_project_team_applicants,
         name='project_teams_applications'),
    path('projects/team/<int:team_pk>/applications/<int:entry_pk>/<str:new_status>',
         views.team_change_status_event_entry_view, name='team_accept_or_deny_applicant'),
]

#project urls
urlpatterns += [
    path('projects/<int:project_pk>/send_notice', views.send_notice, name='project_send_notice'),
    path('projects/<int:project_pk>/send_message/<str:team_pk>', views.send_message, name='project_send_message'),
    path('projects/<int:project_pk>/get_messages_ajax/<str:channel_pk>', views.AjaxGetMessages.as_view(),
         name='ajax_get_messages'),
    path('projects/<int:pk>/applicants', views.look_project_applicants_view, name='check_applicants_for_project'),
    path('projects/<int:project_pk>/applicants/<int:entry_pk>/<str:new_status>', views.change_status_event_entry_view,
         name='accept_or_deny_applicant'),
    path('projects/<int:pk>/participants', views.look_project_participants_view, name='look_participants_of_project'),
    # path('e/<int:pk>/', views.ProjectDetailedView.as_view(), name='project_detail'),
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    ##TODO: RENAME ALL EVENTS TO PROJECTS IN THIS MODULE
    path('projects/my_projects', views.my_projects_view, name='my_projects_list'),
    path('projects/<int:pk>/enter', views.enter_the_project_view, name='enter_the_project_view'),
    # path('projects/create/', views.ProjectCreate.as_view(), name='project_create'),
    path('projects/create/', views.create_project_view, name='project_create'),
    path('projects/pending', views.accept_new_projects_view, name='new_pending_projects_mod'),
    path('projects/pending/<int:pk>/accept', views.accept_project_view, name='accept_project_mod'),
    path('projects/pending/<int:pk>/deny', views.deny_project_view, name='deny_project_mod'),
    path('projects/<int:pk>/update', views.ProjectUpdate.as_view(), name='project_update'),
    path('projects/<int:pk>/delete', views.ProjectDelete.as_view(), name='project_delete'),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]

urlpatterns+=[
    path('myprofile/', views.my_profile_view, name='my_profile'), #eto zaglushka
    path('projects/<int:pk>/finish', views.finish_project_view, name='finish_project'),
]


