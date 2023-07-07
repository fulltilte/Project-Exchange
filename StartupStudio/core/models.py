from django.urls import reverse
from django.utils import timezone

from django.db import models

from UserSystem.models import CustomUser


class Direction(models.Model):
    direction_name = models.CharField(max_length=100)
    direction_info = models.CharField(max_length=800, blank=True)

    def __str__(self):
        return self.direction_name


class EventType(models.Model):
    event_type_name = models.CharField(max_length=50)
    event_type_info = models.CharField(max_length=800, blank=True)

    def __str__(self):
        return self.event_type_name


class Skill(models.Model):
    skill_name = models.CharField(max_length=80)
    skill_info = models.CharField(max_length=800, blank=True)

    def __str__(self):
        return self.skill_name


#Deprecated?
class EntryStatus(models.Model):
    entry_name = models.CharField(max_length=80)

    def __str__(self):
        return self.entry_name


class Team(models.Model):
    team_name = models.CharField(max_length=80)
    team_members = models.ManyToManyField(CustomUser, related_name="team_members")
    team_captain = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL, related_name="team_captain")
    team_info = models.CharField(max_length=800, null=True, blank=True)
    team_lfg_message = models.CharField(max_length=800, null=True, blank=True)
    is_looking_for_group = models.BooleanField(default=False)

    def __str__(self):
        return self.team_name


class Project(models.Model):
    project_name = models.CharField(max_length=150)
    project_info = models.CharField(max_length=1500)
    event_type = models.ForeignKey(EventType, null=True, on_delete=models.SET_NULL)
    direction_type = models.ForeignKey(Direction, null=True, on_delete=models.SET_NULL)
    project_skills = models.ManyToManyField(Skill)

    project_authors = models.ManyToManyField(CustomUser, related_name="project_authors")
    project_participants = models.ManyToManyField(CustomUser, blank=True, null=True, related_name="project_participants")
    project_teams = models.ManyToManyField(Team, blank=True)
    maximum_members_in_team = models.IntegerField(default=4)

    pub_date = models.DateTimeField('Date Time published', default=timezone.now())
    project_start = models.DateTimeField('Project Start')
    project_end = models.DateTimeField('Project Ending')

    # project status should be mad of lists

    PROJECT_STATUS = (
        ('pen', 'На рассмотрении'), ('acc', 'Принято'), ('den', 'Отклонено'), ('act', 'Активно'), ('fin', 'Завершено'))

    project_status = models.CharField(max_length=3, choices=PROJECT_STATUS, blank=True, default='pen',
                                      help_text="Current project status")

    def __str__(self):
        return self.project_name

    def get_absolute_url(self):
        return reverse('core:project_detail', args=[int(self.id)])

    class Meta:
        permissions = [
            ("can_manage_projects", "Can manage projects"),
            ("can_moderate_projects", "Can moderate incoming projects"),
            ("can_create_projects", "Can create projects"),
        ]
        ordering = ['project_start'] #take a notice, that this operation could be costly,
    #consider swapping it to order_by on related controllers
    #ordering is being called every query is called, that also includes foreignkeys and many-to-many fields


class ProjectEntry(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('Время, когда заяка была отправлена', default=timezone.now()) #use timezone.now() to apply default state to the date field
    status_changed_date = models.DateTimeField('Время, когда статус заявки был изменен', default=timezone.now())

    ENTRY_STATUS = (('pen', 'На рассмотрении'), ('acc', 'Заявка одобрена'), ('den', 'Заявка отклонена'))
    status = models.CharField(max_length=3, choices=ENTRY_STATUS, blank=True, default='pen',
                              help_text="Current entry status")

    def __str__(self):
        return self.project.project_name

    #this type of ordering uses too many resources, so probably it's better to move it to the other place
    #class Meta:
    #    ordering = ['-status']


class ProjectResult(models.Model):
    project = models.ForeignKey(Project, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
    project_result = models.CharField(max_length=150)
    users_team = models.CharField(max_length=80)

    def __str__(self):
        return self.project_result


class ProjectChatMessage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
    message_text = models.CharField(max_length=800) #FOR FUTURE: Calling fields like this: MODEL_TEXT proved kinda inconvinient
    pub_datetime = models.DateTimeField('Date published')   #might as well do just "text" next time, so models are easier to swap between

    def __str__(self):
        return self.message_text


class TeamChatMessage(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
    message_text = models.CharField(max_length=800)
    pub_datetime = models.DateTimeField('Date published')

    def __str__(self):
        return self.message_text


class TeamEntry(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    ENTRY_STATUS = (('pen', 'Рассматривается'), ('acc', 'Принято'), ('den', 'Отклонено'))
    status = models.CharField(max_length=3, choices=ENTRY_STATUS, blank=True, default='pen',
                              help_text="Current entry status")

    def __str__(self):
        return self.user.username + " to " + self.team.team_name

# Create your models here.


class ProjectNotice(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    notice_text = models.CharField(max_length=800)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True)
    pub_datetime = models.DateTimeField(default=timezone.now())


