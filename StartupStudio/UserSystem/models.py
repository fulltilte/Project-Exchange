from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.Model):
    role_name = models.CharField(max_length=30)
    role_description = models.CharField(max_length=800)

    def __str__(self):
        return self.role_name

class CustomUser(AbstractUser):
    user_mask_name = models.CharField(max_length=30, blank=True, null=True)
    user_bio = models.CharField(max_length=300, blank=True, null=True)
    roles = models.ManyToManyField(Role) #One user could have many roles
    pass

    #ALWAYS USE THIS METHOD TO GET A NAME OF A USER"S MASK, AS MASK COULD BE EMPTY BUT ALWAYS PREFERRED
    def get_name(self):
        if self.user_mask_name:
            return self.user_mask_name
        else:
            return self.username
 #   user_name = models.CharField(max_length=30)
  #  user_bio = models.CharField(max_length=300)
    #Additional functionality could be added here
# Create your models here.
