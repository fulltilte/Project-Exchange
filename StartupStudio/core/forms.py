import datetime


from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.forms import UserCreationForm
# Create your forms here.
from django.core.exceptions import ValidationError

from django.forms import ModelForm, DateInput

from UserSystem.models import CustomUser
from core.models import Project, Team


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CreateProjectForm(ModelForm):
    #project_start = forms.DateTimeField()
    #datetime forms compatible with xdsoft timepicker and Europe time formats:
    project_start = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'], widget=forms.DateInput(format='%d.%m.%Y %H:%i'), label="Начало проекта")
    project_end = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'],
                                        widget=forms.DateInput(format='%d.%m.%Y %H:%i'), label="Конец проекта")
    class Meta:
        model = Project
        fields = ['project_name', 'project_info', 'event_type', 'direction_type', 'project_skills', 'project_start',
                  'project_end', ]
        labels = {'project_name': 'Название проекта', 'project_info': 'Информация о проекте',
                  'event_type': 'Тип проекта', 'direction_type': 'Название направления', 'project_skills': 'Навыки мероприятия',
                  'project_start': 'Начало проекта', 'project_end': 'Конец проекта'}
        widgets = {
            #'project_end': AdminDateWidget(),
        }

    def clean_project_end(self):
        data = self.cleaned_data['project_end']
        if data.date() < datetime.date.today():
            raise ValidationError('Время конца не может быть в прошлом')
        if self.cleaned_data['project_start'].date() >= self.cleaned_data['project_end'].date():
            if self.cleaned_data['project_start'].date() == self.cleaned_data['project_end'].date() and (self.cleaned_data['project_start'].time()) >= self.cleaned_data['project_end'].time():
                raise ValidationError('Время конца проекта должно быть хотя бы на минуту позже начала')
            else: #if the same date, but starts earlier than ends
                return data
            raise ValidationError('Проект не может заканчиваться раньше, чем начнется')
        return data

    def clean_project_start(self):
        data = self.cleaned_data['project_start']
        if data.date() < datetime.date.today():
            raise ValidationError('Время начала не может быть в прошлом')
        return data


class CreateTeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ['team_name', 'team_info', 'team_lfg_message', 'is_looking_for_group']
        labels = {'team_name':'Название команды', 'team_info':'Информация о команде', 'is_looking_for_group':'Открывать ли команду для поиска участников', 'team_lfg_message':'Сообщение в канал поиска участников'}

