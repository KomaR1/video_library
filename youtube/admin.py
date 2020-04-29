from django.contrib import admin
from .models import Video, Comment, Complain
# Register your models here.

admin.site.register([Video, Comment, Complain])
