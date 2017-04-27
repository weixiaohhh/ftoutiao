from django.contrib import admin
from .models import Profile, Friendship, Subscription, Subject


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']
admin.site.register(Profile, ProfileAdmin)

admin.site.register(Friendship)
admin.site.register(Subscription)
admin.site.register(Subject)


