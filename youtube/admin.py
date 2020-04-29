from django.contrib import admin
from .models import Video, Comment, Complain, UserProfile
# Register your models here.

admin.site.register([Video, Comment, Complain, UserProfile])
