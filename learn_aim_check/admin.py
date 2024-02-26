from django.contrib import admin

from .models import ActionCompetence, LearnAim, Tag

admin.site.register(Tag)
admin.site.register(ActionCompetence)
admin.site.register(LearnAim)
