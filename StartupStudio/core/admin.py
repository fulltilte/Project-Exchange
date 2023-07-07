from django.contrib import admin

from .models import Direction
from .models import EventType
from .models import Skill
from .models import EntryStatus
from .models import Team
from .models import Project
from .models import ProjectEntry
from .models import ProjectResult
from .models import ProjectChatMessage
from .models import TeamChatMessage
from .models import TeamEntry
from .models import ProjectNotice

admin.site.register(EventType)
admin.site.register(EntryStatus)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_filter = ('event_type', 'project_status') #using filters for admin panel
    list_display = ('project_name', 'event_type', 'direction_type')


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('skill_name', 'skill_info')


@admin.register(Direction)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('direction_name', 'direction_info')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'team_captain')


@admin.register(TeamEntry)
class TeamEntry(admin.ModelAdmin):
    list_display = ('team', 'user')


@admin.register(ProjectNotice)
class ProjectNotice(admin.ModelAdmin):
    list_display = ('notice_text', 'user', 'project')


@admin.register(TeamChatMessage)
class TeamChatMessage(admin.ModelAdmin):
    list_display = ('message_text', 'user', 'team')

@admin.register(ProjectChatMessage)
class TProjectChatMessage(admin.ModelAdmin):
    list_display = ('message_text', 'user', 'project')


admin.site.register(ProjectEntry)
admin.site.register(ProjectResult)





