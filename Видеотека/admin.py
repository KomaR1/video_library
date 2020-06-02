from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Video, Comment, Complain, CustomUser, Genre


# Register your models here.


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (  # new fieldset added on to the bottom
            'Custom Field Heading',  # group heading of your choice; set to None for a blank space instead of a header
            {
                'fields': (
                    'birth',
                ),
            },
        ),
    )


admin.site.register([Genre])
admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'views', 'user', 'genre')
    search_fields = ('views', 'description')
    raw_id_fields = ('user',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'datetime')
    search_fields = ('text', 'datetime')


@admin.register(Complain)
class ComplainAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'text', 'datetime', 'state')

