import datetime

from django.contrib.auth.models import User, Permission, Group
from django.db import models
from schools.models import School

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="member")
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Member: {self.user.email}"