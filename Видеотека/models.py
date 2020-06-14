from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    birth = models.DateField('Дата рождения', null=True, blank=True)

    class Meta:
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'


class Genre(models.Model):
    genre = models.CharField('Жанр', max_length=20, help_text='Введите жанр видео', unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.genre


class Video(models.Model):
    title = models.CharField('Название', max_length=30)
    description = models.TextField('Описание', max_length=300)
    path = models.CharField('Путь', max_length=300)
    datetime = models.DateTimeField('Дата и время', auto_now=True, blank=False, null=False) #todo: auto_now=True
    views = models.PositiveIntegerField('Просмотры', default=0)
    user = models.ForeignKey('Видеотека.CustomUser', on_delete=models.CASCADE, related_name='users',
                             verbose_name='Пользователь')
    genre = models.ForeignKey('Видеотека.Genre', on_delete=models.CASCADE, verbose_name=('Жанр'))

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'


class Comment(models.Model):
    text = models.TextField('Текст', max_length=300)
    datetime = models.DateTimeField('Дата и время', auto_now=True, blank=False, null=False)
    user = models.ForeignKey('Видеотека.CustomUser', on_delete=models.CASCADE, verbose_name='Пользователь')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='videos')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Complain(models.Model):
    user_id = models.ForeignKey('Видеотека.CustomUser', on_delete=models.CASCADE, related_name='user_ids')
    text = models.TextField('Текст', max_length=300)
    datetime = models.DateTimeField('Дата и время', auto_now=True, blank=False, null=False)
    state = models.BooleanField('Выполнен', default=False)

    class Meta:
        verbose_name = 'Жалобу'
        verbose_name_plural = 'Жалобы'
