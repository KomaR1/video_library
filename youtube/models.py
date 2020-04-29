from django.db import models
from django.contrib.auth.models import User


# class UserProfile(models.Model):
#   user = models.OneToOneField(User, on_delete=models.CASCADE)
#   full_name = models.CharField(max_length=60)
#   birth = models.DateField()


class Video(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=300)
    path = models.CharField(max_length=60)
    datetime = models.DateTimeField(auto_now=True, blank=False, null=False) #todo: auto_now=True
    views = models.PositiveIntegerField(default=0)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.TextField(max_length=300)
    datetime = models.DateTimeField(auto_now=True, blank=False, null=False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)


class Complain(models.Model):
    user_id = models.ForeignKey('auth.user', on_delete=models.CASCADE)
    text = models.TextField(max_length=300)
    datetime = models.DateTimeField(auto_now=True, blank=False, null=False)
    state = models.BooleanField(default=False)
