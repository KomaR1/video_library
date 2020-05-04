from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=60, help_text='Enter your full name')
    birth = models.DateField(null=True, blank=True)


class Genre(models.Model):
    genre = models.CharField(max_length=20, help_text='Enter a video genre', unique=True)

    def __str__(self):
        return self.genre

    class Meta:
        verbose_name = 'genre'
        verbose_name_plural = 'genres'


class Video(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=300)
    path = models.CharField(max_length=60)
    datetime = models.DateTimeField(auto_now=True, blank=False, null=False) #todo: auto_now=True
    views = models.PositiveIntegerField(default=0)
    user = models.ForeignKey('youtube.CustomUser', on_delete=models.CASCADE, related_name='users')
    genre = models.ForeignKey('youtube.Genre', on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.TextField(max_length=300)
    datetime = models.DateTimeField(auto_now=True, blank=False, null=False)
    user = models.ForeignKey('youtube.CustomUser', on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='videos')


class Complain(models.Model):
    user_id = models.ForeignKey('youtube.CustomUser', on_delete=models.CASCADE, related_name='user_ids')
    text = models.TextField(max_length=300)
    datetime = models.DateTimeField(auto_now=True, blank=False, null=False)
    state = models.BooleanField(default=False)
