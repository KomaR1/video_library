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
                    'full_name',
                    'birth'
                ),
            },
        ),
    )


admin.site.register([Video, Comment, Complain, Genre])
admin.site.register(CustomUser, CustomUserAdmin)
