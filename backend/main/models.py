from django.db import models
from django.contrib.auth.models import User


class Staff(models.Model):
    ADM = 'ADM'
    TECH = 'TECH'
    POSTS = [
        (ADM, 'Администратор'), (TECH, 'Техник')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    father_name = models.CharField(max_length=150, null=True, blank=True)
    post = models.CharField(max_length=50, choices=POSTS, default=TECH)
