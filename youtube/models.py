from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=60)
    #birth = models.DateField()

    # def __unicode__(self):
    #     return self.user


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


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
