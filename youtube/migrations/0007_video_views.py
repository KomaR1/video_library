# Generated by Django 3.0.5 on 2020-04-29 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('youtube', '0006_complain'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
