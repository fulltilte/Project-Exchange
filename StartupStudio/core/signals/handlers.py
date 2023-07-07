from django.contrib.auth.models import Group


def add_to_default_group(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        group = Group.objects.get(name='Организатор') #this signal adds Organiser role to the user upon creating one
        user.groups.add(group)
